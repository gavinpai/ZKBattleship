# ZKBattleship

## Summary

In online gaming, there has been a lot of excitement around games hosted on home servers rather than on conventional gaming platforms; gamers are becoming creators, building their own games that they host on their own PCs, leveraging platforms like Twitch or YouTube to stream and establish personal brand. In many of these games, there is a secret such as position on a map that must be concealed, but also conform to a set of bounds. Battleship is a test case of a protocol that will also be applicable to complex games such as First-Person Shooters. The problems that were solved included proving the correctness of a ship arrangement and revealing ship locations at will in Battleship without giving knowledge of any other ship locations to an opponent. A Kolmogorov-Smirnov test, which is a test to determine if two samples have the same statistical distribution, was conducted on each variable for at least 100,000 outputs of the proof of correctness that I designed for the ship configuration were shown with a p-value of at least 0.36 to be of the same distribution no matter where the ships were on the board, which means that an opponent will not learn anything about the placement of a player’s ships, whereas a p-value of less than 0.1 would have shown that the distributions were different. The protocol works as intended, however having ships occupy multiple spaces so that cheating is prevented has not been implemented, which could be attempted for further research.

## Details

The problem this project aimed to solve was making a game of Battleship where each player can ensure that the other is not cheating in real time. This may sound easy; however, an additional limitation present is that there can be no trusted agent to check each board. Therefore, no one but the person who created the arrangement of ships can know where each ship is until they choose to reveal that information.

Your first instinct for solving this problem may be something like using a cryptographic hash function on each board space and sending that prior to playing the game. The problem with this is that if the input space is small, the output space will also be small for a cryptographic hash function. Given that the inputs will always be a one or a zero, it would be very easy to tell what each space is. Another issue with this is one could put in bogus input of ships and the other player would not know in real time that the opposing player was cheating, wasting their time.

The solution to the first problem, where small input space will lead to small output space, is creating a one-way function that also has a blinding factor to ensure that the function is not deterministic. Instead of one output being needed to create an output, two will be needed, and likewise for verifying that the output matches the input. The two inputs are a random blinding factor and the actual message. The way this has been implemented is through a Pedersen commitment, which relies on the discrete logarithm assumption. The useful property of Pedersen commitments to solve the first problem is that Pedersen commitments are unconditionally concealing, which means that the output value distribution of a Pedersen commitment generator is uniform. A second useful property of Pedersen commitments is that they are binding, which means that it is hard to find another set of inputs that will generate the same commitment value.

The final useful property of the Pedersen commitment used for this program is that it is homomorphic. This means that if one adds one Pedersen commitment with another, a new valid commitment is made with an underlying value of the two commitments' values. For example, one can add a commitment that encodes for one and a commitment that encodes for two and a verifier could know the sum, the combined commitments, and the combined blinding factors and they would be able to verify that both commitments add up to three. They are able to verify this sum without any knowledge of the values of the commitments, the input values, or the blinding factors.

This comes into play when trying to see if the correct number of ships are on the board. What I did was publish the commitments but not the blinding factors at the start of the game, along with a sum proof. This proof was the addition of the commitment of every square on the board. The other player knows the combined blinding factors, commitments, and knows that the underlying values of the squares will add to eight, or any arbitrary number of ships. The other player can verify that this is a valid commitment and know that the other player has the right number of ships. There is one small problem here though. If the cheating player were to input random numbers that added to eight, such as having two spaces on the board equal four and the rest zero, the honest player would not know until they picked that square. In short, it needs to be proved that all square values are bits and not arbitrary numbers.

This was solved through a novel approach to the Schnorr protocol. The Schnorr protocol is a proof of knowledge of the discrete logarithm without actually revealing the discrete logarithm. It does this through the introduction of a challenge scalar which can be sent from the verifier to the prover. The intuition behind the challenge scalar is that one can only perform a certain operation with the challenge scalar if one knows the discrete logarithm. If you remember from earlier, the Pedersen commitment relies on the discrete logarithm assumption. Proof of knowledge of the Pedersen commitment message can be mathematically manipulated into a proof of knowledge of a discrete logarithm. So, one player can prove to another that each bit is a zero or a one. The problem here is that the proof for proving that a message is zero is different than that for one, so the verifier can tell what the value of each space is for this scheme.

The way to solve for this lies with the challenge scalar. If the challenge scalar can be manipulated, a prover can prove a wrong statement. This is useful as two proofs can be built, one to prove that the value is zero and one to prove that the value is one. If the challenge scalar can be decided for one of those and the other is actually true, the prover can send the verifier a proof that the commitment is either zero or one. This is done by the prover deciding one challenge scalar and the verifier deciding what both challenge scalars add up to so that the prover can only manipulate one challenge scalar, and the verifier does not know which. The proof for when the value is zero and when it is one are indistinguishable to the verifier.

One final nuance to this project is that the challenge scalar is not actually chosen by the verifier. It is instead computed using a Fiat-Shamir heuristic. This is a way to make an interactive zero-knowledge proof where a verifier supplies a challenge scalar to a non-interactive zero-knowledge proof. This is done through using a cryptographic hash function on what would be the first message of the interactive proof to determine the challenge scalar.

The specific modules that make up this package and a few specific implementation details are provided below, albeit mostly in less depth. All code is my own, and only the standard library was used for the protocol itself. The statistics module is the only module that requires additional libraries.

More details about Pedersen Commitments, the Schnorr Protocol and the Fiat-Shamir Heuristic can be found in the following links: 

https://link.springer.com/chapter/10.1007/3-540-46766-1_9

https://link.springer.com/article/10.1007/BF00196725

https://link.springer.com/chapter/10.1007/3-540-47721-7_12

## Implementation Details

### Adaptable modules (useful for other cases)
 
#### random_prime.py

The random prime module's function is to return a random prime that fits certain sets of constraints depending on which function is called, such as the length of the prime in bits or if a prime of the form 4 * x + 1 is also a prime. It does so by finding a random odd number with the bit length specified and adding two until it is prime under a set of primality tests. These include the Fermat and Miller-Rabin primality tests.

#### pedersen.py 
This class was meant to generate, hold, create generators for, add, and verify Pedersen commitments. Rather than holding the Pedersen generator as an instance of the Pedersen class, Pedersen generators are instead held as data classes inside the Pedersen class for ease of transporting values and referencing internal variables. The commitment outputs are held the same way. Rather than using an instance of the Pedersen class, most operations are done statically and through arguments.

#### bitproof.py

This module implements a modified Schnorr protocol to prove knowledge of the message in a commitment was a bit. This protocol was modified such that one could cheat to prove that the value of the commitment was both a zero and a one if the value were either a zero or a one, giving the verifier zero knowledge of the message except that it is a bit. A Fiat-Shamir heuristic was also implemented to make the proof non-interactive and easier to implement. This proof is also held in a data class for ease of transporting values and referencing the many variables in the proof.

### Case specific modules (useful for Battleship only) 

#### board.py 

In the board module, each board that would be used in the actual Battleship was designed. First, a board class that all others would be inherited from was programmed with the methods to return a spot on the board given a Battleship coordinate. Then, boards for specific purposes, like holding public commitments or responses from the other player, were made. Finally, a shipboard was made that inherited from the commitment board such that it could hold the commitments and spaces parallel to each other. The commitment board contains the functionality to create commitments and proofs for those commitments while the other two boards contain the functionality to return the board as a string and toggle a space. 

#### \_\_main__.py 

Finally, the main program was written. I designed a player class such that, theoretically, the two players can play online and there is a degree of encapsulation. It was asynchronous so that one player could wait for another player to input their board or do their turn without making IO operations broken. First, both players input their board, and then the game starts. Each player has the other player instance as a variable so that they can call a function to get the value of, say, a specific square. Players take turns asking squares until all ships are found. 

### stats.py 

This module can be safely ignored. It is only for my personal use of analyzing the distributions of bit proofs or commitments and making graphs for my posterboard. This is the only module that uses libraries outside of the standard library. MatPlotLib and SciPy are not needed if this module is not used. 

