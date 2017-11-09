#!/usr/bin/env node

import * as fs from "async-file";
import readFile = require('fs-readfile-promise');
import asyncMkdirp = require('async-mkdirp');
import * as path from "path";
import * as recursiveReadDir from "recursive-readdir";
import { CompilerInput, CompilerOutput, compileStandardWrapper } from "solc";
import { Configuration } from './Configuration';

export class ContractCompiler {
    private readonly configuration: Configuration;

    public constructor(configuration: Configuration) {
        this.configuration = configuration
    }

    public async compileContracts(): Promise<CompilerOutput> {
        // Check if all contracts are cached (and thus do not need to be compiled)
        try {
            const stats = await fs.stat(this.configuration.contractOutputPath);
            const lastCompiledTimestamp = stats.mtime;
            const ignoreCachedFile = function(file: string, stats: fs.Stats): boolean {
                return (stats.isFile() && path.extname(file) !== ".sol") || (stats.isFile() && path.extname(file) === ".sol" && stats.mtime < lastCompiledTimestamp);
            }
            const uncachedFiles = await recursiveReadDir(this.configuration.contractSourceRoot, [ignoreCachedFile]);
            if (uncachedFiles.length === 0) {
                return JSON.parse(await fs.readFile(this.configuration.contractOutputPath, "utf8"));
            }
        } catch {
            // Unable to read compiled contracts output file (likely because it has not been generated)
        }

        // Compile all contracts in the specified input directory
        const compilerInputJson = await this.generateCompilerInput();
        const compilerOutputJson = compileStandardWrapper(JSON.stringify(compilerInputJson));
        const compilerOutput: CompilerOutput = JSON.parse(compilerOutputJson);
        if (compilerOutput.errors) {
            let errors = "";
            for (let error of compilerOutput.errors) {
                errors += error.formattedMessage + "\n";
            }
            throw new Error("The following errors/warnings were returned by solc:\n\n" + errors);
        }
        const filteredCompilerOutput = this.filterCompilerOutput(compilerOutput);

        // Create output directory (if it doesn't exist)
        await asyncMkdirp(path.dirname(this.configuration.contractOutputPath));

        // Output contract data to single file
        const contractOutputFilePath = this.configuration.contractOutputPath;
        await fs.writeFile(contractOutputFilePath, JSON.stringify(filteredCompilerOutput, null, '\t'));

        return filteredCompilerOutput;
    }

    public async generateCompilerInput(): Promise<CompilerInput> {
        const ignoreFile = function(file: string, stats: fs.Stats): boolean {
            return file.indexOf("legacy_reputation") > -1 || (stats.isFile() && path.extname(file) !== ".sol");
        }
        const filePaths = await recursiveReadDir(this.configuration.contractSourceRoot, [ignoreFile]);
        const filesPromises = filePaths.map(async filePath => (await readFile(filePath)).toString('utf8'));
        const files = await Promise.all(filesPromises);

        let inputJson: CompilerInput = {
            language: "Solidity",
            settings: {
                optimizer: {
                    enabled: true,
                    runs: 500
                },
                outputSelection: {
                    "*": {
                        "*": [ "abi", "evm.bytecode.object" ]
                    }
                }
            },
            sources: {}
        };
        for (var file in files) {
            const filePath = filePaths[file].replace(this.configuration.contractSourceRoot, "").replace(/\\/g, "/");
            inputJson.sources[filePath] = { content : files[file] };
        }

        return inputJson;
    }

    private filterCompilerOutput(compilerOutput: CompilerOutput): CompilerOutput {
        const result: CompilerOutput = { contracts: {} };
        for (let relativeFilePath in compilerOutput.contracts) {
            for (let contractName in compilerOutput.contracts[relativeFilePath]) {
                // don't include helper libraries
                if (!relativeFilePath.endsWith(`${contractName}.sol`)) continue;
                const abi = compilerOutput.contracts[relativeFilePath][contractName].abi;
                if (abi === undefined) continue;
                const bytecodeString = compilerOutput.contracts[relativeFilePath][contractName].evm.bytecode.object;
                if (bytecodeString === undefined) continue;
                // don't include interfaces
                if (bytecodeString.length === 0) continue;
                result.contracts[relativeFilePath] = {
                    [contractName]: {
                        abi: abi,
                        evm: { bytecode: { object: bytecodeString } }
                    }
                }
            }
        }
        return result;
    }
}
