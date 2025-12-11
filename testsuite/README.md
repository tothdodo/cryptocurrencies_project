# Testcases for VU Cryptocurrencies, W2025, TU Wien

Copyright (C) 2025 Thomas Ogrisegg. Comments, patches, suggestions, additional test cases etc. can be sent to (tom-bugs-cc (at) fnord.at)

The test suite can be downloaded [here](https://fnord.at/ccw25/testsuite.tgz)

Testcases for Task 3 can be downloaded [here](https://fnord.at/ccw25/tests3.tgz)

Testcases for Task 4 can be downloaded [here](https://fnord.at/ccw25/tests4.tgz)
(note: the test cases in the Task4\_freshdb directory need to be run on a freshly initialized database or else they will fail)

## Updates

    251130: v.py was missing in the testsuite.tgz file. Added
    251202: Added test cases for Task4. Adapted runtest.py to include chaintip/getchaintip command in 'objects' and fixed a few bugs. Task3's unknown_object test case had the wrong height: corrected

## Overview

This suite includes two python scripts:

    gentest.py: generates test cases and writes them into json files
    runtest.py: runs the json test files against a server

### TLDR

Extract the test cases linked above, start your server, and then run

> python ./runtest.py *.json

in the directory you extracted the test cases to

NB: the test case archive linked above contains a few more test cases,
than can be generated with the test suite, as they were handcrafted

### Overview of gentest.py

**Syntax:**

> python gentest.py testcasefile [test cases to generate]

Example:

**generates all tests in testcase1.py**

> python ./gentest.py testcase1 

**generates only the test cases invalid_previd and unknown object
 in testcase1.py**

> python ./gentest.py testcase1 invalid\_previd unknown\_object

The generated test cases in the latter case are called invalid\_previd.json
and unknown\_object.json

### Overview of runtest.py

We can now run these test cases. Start your server and then run:

Syntax:

> python runtest.py testfile.json [testfile2.json [...]]

For the above generated file the syntax would be:

>  python ./runtest.py invalid\_previd.json unknown\_object.json

The runtest.py script will connect to your server on localhost:18018
and execute all the tests with the failed tests being highlighted

NB: If your terminal doesn't support ANSI color codes or you don't have
the colorterm python module then simply set 'colored = 0' at the beginning
of the runtest.py file

### Writing test cases

Writing your own test cases is easy. v.py includes many useful functions
to create your own blocks and transactions.

Use the following as a template:

**newtest case.py**

      from v import *
     
      coinbase_trans = {"object":{"height":1,"outputs":[{"pubkey":pubkeys[0],"value":50000000000000}],"type":"transaction"},"type":"object"}
     
      def gen_test_foobar():
          description = "This is the foobar test case"
          block1 = mkBlock(None, [coinbase_trans], description)
          mine(block1)
          transaction = mkTrans([transIn(0,coinbase_trans)], [transOut(1, 500000), transOut(2, 50000)])
          full_signature(0, transaction)
          block2 = mkBlock(block1, [transaction], description)
          return {
             'description': description,
             'objects': [ coinbase_trans, (block1,True), transaction, (block2,True) ]
          }
     

Let's go through this line by line:

> def gen\_test\_foobar():

Every test case has to start with "gen\_test\_". The string after that will
be used for the .json output filename (in this case "foobar.json")

> description = "This is the foobar test case"

Begin with a description, what does this test case do, what does it test?

> block1 = mkBlock(None, [coinbase\_trans], description)

This generates a new block. The first parameter is the previous block (if
None is passed then the Genesis Block is used), after that the transactions
in the block, in this case only the first coinbase transaction above.

Then a description that will be put into the note of the block to 
distinguish blocks more easily while debugging.

After that we have to

>     mine(block1)

mine the block so that we can reference it later. This just sets the
correct nonce field

>     transaction = mkTrans([transIn(0,coinbase_trans)], [transOut(1, 500000), transOut(2, 50000)])

This creates a new transaction, with the Input transactions being made
via the transIn function that takes an index and a previous transaction
as parameter, so here coinbase and the index as the first parameter
(which is in this case 0 as with all coinbase transactions)

The generator script provides 10 public/private key pairs that you can
use as wallets.

The transOut function takes an index of these key pairs as the first
parameter and the value that should be transfered to this wallet as the
second. So in this case we transfer 500000 to Wallet 1 and 50000 to
Wallet 2. The original coinbase transaction was transfered to Wallet 0

>     full_signature(0, transaction)

We now have to sign the transaction with the key of the input
transaction(s), which was the original coinbase transaction and Wallet 0

>     block2 = mkBlock(block1, [transaction], description)

Now we create the second block, we set the first block as the parent and
put the newly created transaction in the transaction list

Note that we do not call mine(block2) as it's not necessary since block2
is not referenced later. If we created a third block that has block2 as
its parent we would have had to call mine(block2) so that the correct
hash for block2 would be available

>     return {
>        'description': description,
>        'objects': [ coinbase_trans, (block1,True), transaction, (block2,True) ]
>     }

we now return the whole test case, this contains all the transactions and
blocks that are being used. For every object that should be sent to the
server we use a tuple (in this case for the two blocks). The second part
of the tuple is a boolean that tells the runtest script whether it
should check if this block was actually correctly stored by the server.
We should do this with every valid block, while we mustn't do it with an
invalid block since that block must not exist on the server.

So in this case the runtest script will send block1, check that block1
is indeed correctly stored by the server and later send block2 and check
that it is correctly stored by the server as well.

If the block2 block was invalid we would rather have written
(block2,False)
