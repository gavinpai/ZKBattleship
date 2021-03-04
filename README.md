# CSRSEF
This project was built to demonstrate a protcol to play Battleship without a trusted party. In this project, multiple modules have been created to fulfill this task, and all code is my own. I will go over each module in the following sections. 

## Adaptable modules (useful for other cases)

### random_prime.py
The random prime module was the first one I had designed. It's function is to return a random prime that fits certain sets of constrainst depending on which function is called, such as the length of the prime in bits or if a prime of the form 4 * x + 1 is also a prime. It does so by finding a random odd number with the bit length specified and adding two until it is prime under a set of primality tests. These include the Fermat and Miller-Rabin primality tests.

### pedersen.py
Next, I designed the pedersen module because it had use with bulletproofs, my initial design idea. This class was meant to generate, hold, create generators for, add, and verify Pedersen commitments (https://link.springer.com/chapter/10.1007/3-540-46766-1_9). Rather than holding the Pedersen generator as an instance of the pedersen class, Pedersen generators are instead held as dataclasses inside the the Pedersen class for ease of transporting values and referencing internal variables. The commitment outputs are held the same way. Rather than using an instance of the Pedersen class, most operations are done statically and through arguments.

### bitproof.py
This module implements a modified Schnorr protocol (https://link.springer.com/article/10.1007/BF00196725) to prove knowledge of the message in a commitment was a bit. This protocol was modified such that one could cheat to prove that the value of the commitment was both a zero and a one if the value was either, giving the verifier zero knowledge of the message except that it is a bit. A Fiat-Shamir heuristic (https://link.springer.com/chapter/10.1007%2F3-540-47721-7_12) was also implemented to make the proof non interactive and easier to implement. This proof is also held in a data class for ease of transporting values and referencing the many variables in the proof.

## Case specific modules (useful for Battleship only)

## board.py
In the board module, each board that would be used in the actual Battleship was designined. First a board class that all others would be inherited from was programmed with the methods to return a spot on the board given a Battleship coordinate...
