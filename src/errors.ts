import { ErrorNameType } from './message'

export class CustomError extends Error {
    name: ErrorNameType
    isNonFatal: Boolean
    missingTXIDs: Set<string>

    constructor(msg: string, name: ErrorNameType, isNonFatal: boolean = false, missingTXIDs: Set<string> = new Set()) {
        super(msg);

        // Set the prototype explicitly.
        Object.setPrototypeOf(this, CustomError.prototype);

        this.name = name
        this.isNonFatal = isNonFatal
        this.missingTXIDs = missingTXIDs
    }

    getErrorName(): ErrorNameType {
        return this.name
    }

    getMissingTXIDs(): Set<string> {
        return this.missingTXIDs
    }
}