import { strict as assert } from "assert";
import { Peer } from "../src/peer";
import { MessageSocket, network } from "../src/network";
import { testObjects } from "./testobjects";
import { objectManager } from "../src/object";
import { canonicalize } from "json-canonicalize";
import { normalize } from "../src/crypto/hash";

const BIND_PORT = 18018
const BIND_IP = '0.0.0.0'

async function delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function main() {
    console.log("🧪 Starting simple network test...");

    // Create a network
    await network.init(BIND_PORT, BIND_IP)
    console.log("✅ Network started on port 18018");

    // objectManager.putTest(
    //     'g71408bf847d7dd15824574a7cd4afdfaaa2866286910675cd3fc371507aa196',
    //     {
    //         "type": "transaction",
    //         "inputs": [
    //             {
    //                 "outpoint": {
    //                     "txid": "6ebfb4c8e8e9b19dcf54c6ce3e1e143da1f473ea986e70c5cb8899a4671c933a",
    //                     "index": 0
    //                 },
    //                 "sig": "3869a9ea9e7ed926a7c8b30fb71f6ed151a132b03fd5dae764f015c98271000e7da322dbcfc97af7931c23c0fae060e102446ccff0f54ec00f9978f3a69a6f0f"
    //             }
    //         ],
    //         "outputs": [
    //             {
    //                 "pubkey": "077a2683d776a71139fd4db4d00c16703ba0753fc8bdc4bd6fc56614e659cde3",
    //                 "value": 5100000000
    //             }
    //         ]
    //     }
    // )

    // const savedObjects = await objectManager.getAll();
    // console.log(`📦 Loaded ${savedObjects.length} objects from the database.`);
    // console.log("📦 All objects:\n", JSON.stringify(savedObjects, null, 2));
    // console.log("DB/---------------------------------------------------------------")
    // // Broadcast objects to peers
    // for (let o of testObjects) {
    //     const isValid = await objectManager.validate(normalize(o).object);
    //     if (isValid) {
    //         console.log(`✅ Object ${objectManager.id(o)} is valid`);
    //         objectManager.put(o);
    //     } else {
    //         console.log(`❌ Object ${objectManager.id(normalize(o).object)} is invalid`);
    //         console.log(normalize(o).object)
    //     }
    //     console.log("---------------------------------------------------------------")
    //     // modify the "if" so the last element does not wait
    //     if (testObjects.indexOf(o) !== testObjects.length - 1) {
    //         await delay(2000); // slight delay to avoid overwhelming
    //     }
    // }
}

// Run test and catch errors
main().catch(err => {
    console.error("❌ Test failed:", err);
    process.exit(1);
});


// objectManager.putTest(
//         'f71408bf847d7dd15824574a7cd4afdfaaa2866286910675cd3fc371507aa196',
//         {
//             "T": "0000abc000000000000000000000000000000000000000000000000000000000",
//             "created": 1671148800,
//             "miner": " grader",
//             "nonce": "1000000000000000000000000000000000000000000000000000000001aaf999",
//             "note": " This block has a coinbase transaction ",
//             "previd": "0000000052a0e645eca917ae1c196e0d0a4fb756747f29ef52594d68484bb5e2",
//             "txids": ["6ebfb4c8e8e9b19dcf54c6ce3e1e143da1f473ea986e70c5cb8899a4671c933a"],
//             "type": "block"
//         }
//     )
