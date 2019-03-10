<p align="center">
  <img
    src="https://nodis.io/static/media/nodis-logo.abf6b121.png"
    width="125px;">
    
</p>
<h3 align="center">Nodis Smart Contract</h3>
<p align="center">The official Python NODIS Smart Contract.</p>
<hr/>

#Description

This contract has been designed and developed by the NODIS team. It will serve during the token sales and throughout the entire duration of the NODIS project.

#Commands

##Token Sale / ICO

`sc invoke <contract address> crowdsale_status ["<wallet address>"]` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>
&nbsp;&nbsp;&nbsp;&nbsp; - Check that user is registered

`sc invoke <contract hash> mintTokens [] --attach-gas={number}` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>
&nbsp;&nbsp;&nbsp;&nbsp; - Buy NODIS using GAS. **Minimum = 50 GAS**

##Transferring NODIS tokens

`sc invoke <contract address> transfer ["<owner address>", "<destination address>", 500]` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>
&nbsp;&nbsp;&nbsp;&nbsp; - Can only be used by the wallet in `owner address`

##Mining Rate

`sc invoke <contract hash> get_mining_rate []` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>
&nbsp;&nbsp;&nbsp;&nbsp; - **50 NODIS per Challenge** initially, decreases depending on how much is in _CHALLENGE_SYSTEM_RESERVE_.

`sc invoke <contract hash> get_promoter_mining_rate []` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>
&nbsp;&nbsp;&nbsp;&nbsp; - **40 NODIS per Submission** initially, decreases depending on how much is in the _CHALLENGE_SYSTEM_RESERVE_.

`sc invoke <contract hash> get_approver_mining_rate [1]` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>
&nbsp;&nbsp;&nbsp;&nbsp; - **6 NODIS** for **all approvers** initially, decreases depending on how much is in the _CHALLENGE_SYSTEM_RESERVE_.

`sc invoke <contract hash> get_rejecter_mining_rate [1]` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>
&nbsp;&nbsp;&nbsp;&nbsp; - **4 NODIS** for **all rejecters** initially, decreases depending on how much is in the _CHALLENGE_SYSTEM_RESERVE_.

`sc invoke <contract address> transfer ["<admin address>", "b'CHALLENGE_SYSTEM_RESERVE'", 500]` <span style="color:BlueViolet;border-color:BlueViolet;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">ADMIN</span> <span style="color:red;border-color:red;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">BUG</span>
&nbsp;&nbsp;&nbsp;&nbsp; - For the administrator to increase the **challenge reserve**, increasing the mining rate
&nbsp;&nbsp;&nbsp;&nbsp; #404



##Challenge System 

`sc invoke <contract address> register_business ["<business address>"]` <span style="color:BlueViolet;border-color:BlueViolet;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">ADMIN</span>
&nbsp;&nbsp;&nbsp;&nbsp; - For the administrator to **Register** a business

`sc invoke <contract address> signout_business ["<business address>"]` <span style="color:BlueViolet;border-color:BlueViolet;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">ADMIN</span>
&nbsp;&nbsp;&nbsp;&nbsp; - For the administrator to **Unregister** a business

`sc invoke <contract address> create_challenge ["<Alice's address>", 'challenge-number-1']` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span> <span style="color:DarkSlateGrey;border-color:DarkSlateGrey;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">BUSINESS</span>
&nbsp;&nbsp;&nbsp;&nbsp; **Alice** is creating a **Challenge** called **_challenge-number-1_**
&nbsp;&nbsp;&nbsp;&nbsp; - Must be executed from Alice's address. <input type="checkbox" checked disabled>
&nbsp;&nbsp;&nbsp;&nbsp; - Alice must be a Business. <input type="checkbox" checked disabled> _challengeExclusiveTest_
&nbsp;&nbsp;&nbsp;&nbsp; - Cannot be executed more than once a month OR must have _Challenge Package_ count. <input type="checkbox" checked disabled> _challengeOnceAMonth_
&nbsp;&nbsp;&nbsp;&nbsp; - Challenges can not have the same name, if so FAIL. <input type="checkbox" checked disabled> _challengeSameName()_
&nbsp;&nbsp;&nbsp;&nbsp; - Challenges remain open for 30 days or until closed. <input type="checkbox" checked disabled> _challengeCloseTest()_

`sc invoke <contract address> submit ["<Bob's address>", "<Alice's address>", 'challenge-number-1']` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>
&nbsp;&nbsp;&nbsp;&nbsp; **Bob** is submitting to **Alice's** challenge called **_challenge-number-1_**
&nbsp;&nbsp;&nbsp;&nbsp; - Must be executed from Bob's address. <input type="checkbox" checked disabled>
&nbsp;&nbsp;&nbsp;&nbsp; - Bob can be a _User_ or _Business_. <input type="checkbox" checked disabled>
&nbsp;&nbsp;&nbsp;&nbsp; - Bob cannot submit twice. <input type="checkbox" checked disabled> _submitTwiceTest()_
&nbsp;&nbsp;&nbsp;&nbsp; - Alice can submit to her own challenge. <input type="checkbox" checked disabled> _submitToOwnChallenge()_
&nbsp;&nbsp;&nbsp;&nbsp; - If Alice does not exist, submission will FAIL. <input type="checkbox" checked disabled> _submitToNonexistentChallenge()_
&nbsp;&nbsp;&nbsp;&nbsp; - If **_challenge-number-1_** does not exist, submission will FAIL. <input type="checkbox" checked disabled> _submitToNonexistentChallenge()_
&nbsp;&nbsp;&nbsp;&nbsp; - Challenge must not be expired, else submission will FAIL. <input type="checkbox" disabled>
&nbsp;&nbsp;&nbsp;&nbsp; - Challenge cannot be closed, else submission will FAIL. <input type="checkbox" checked disabled> _challengeCloseTest()_
&nbsp;&nbsp;&nbsp;&nbsp; - Submission will FAIL, if Submission MAX for Challenge hit (100 submissions). <input type="checkbox" checked disabled> _testMaxSubmission()_


`sc invoke <contract address> approve_submission ["<David's address>", "<Bob's address>", "<Alice's address>", 'challenge-number-1']` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>
&nbsp;&nbsp;&nbsp;&nbsp; **David** is approving **Bob's** submission to **Alice's** challenge called **_challenge-number-1_**
&nbsp;&nbsp;&nbsp;&nbsp; - Must be executed from David's address. <input type="checkbox" checked disabled>
&nbsp;&nbsp;&nbsp;&nbsp; - David cannot execute twice. <input type="checkbox" checked disabled> _testApproveTwice()_
&nbsp;&nbsp;&nbsp;&nbsp; - Bob can approve his own submission. <input type="checkbox" checked disabled> _testApproveTwice()_
&nbsp;&nbsp;&nbsp;&nbsp; - Submission must not be expired (24hr + 10min), else approval will FAIL <input type="checkbox" disabled>

`sc invoke <contract address> reject_submission ["<Francis' address>", "<Bob's address>", "<Alice's address>", 'challenge-number-1']` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span> 
&nbsp;&nbsp;&nbsp;&nbsp; **Francis** is rejecting **Bob's** submission to **Alice's** challenge called **_challenge-number-1_**
&nbsp;&nbsp;&nbsp;&nbsp; - Must be executed from Francis's address. <input type="checkbox" checked disabled>
&nbsp;&nbsp;&nbsp;&nbsp; - Francis cannot execute twice. <input type="checkbox" checked disabled> _testRejectTwice()_
&nbsp;&nbsp;&nbsp;&nbsp; - Bob can reject his own submission. <input type="checkbox" checked disabled> _testRejectTwice()_
&nbsp;&nbsp;&nbsp;&nbsp; - Submission must not be expired (24hr + 10min), else rejection will FAIL <input type="checkbox" disabled>

`sc invoke <contract address> close_challenge ["<Alice's address>", 'challenge-number-1']` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span> <span style="color:DarkSlateGrey;border-color:DarkSlateGrey;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">BUSINESS</span>
&nbsp;&nbsp;&nbsp;&nbsp; **Alice** is completing her **Challenge** called **_challenge-number-1_**
&nbsp;&nbsp;&nbsp;&nbsp; - Must be executed from Alice's address. <input type="checkbox" checked disabled>
&nbsp;&nbsp;&nbsp;&nbsp; - Challenge must not be expired, else FAIL <input type="checkbox" disabled>
&nbsp;&nbsp;&nbsp;&nbsp; - Challenge cannot be already closed, else FAIL <input type="checkbox" disabled>


##Challenge Package

`sc invoke <contract hash> buy_challenge_package ["<alice_address>", 2]` <span style="color:BlueViolet;border-color:BlueViolet;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">ADMIN</span> <span style="color:DarkSlateGrey;border-color:DarkSlateGrey;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">BUSINESS</span>
&nbsp;&nbsp;&nbsp;&nbsp; Businesses can buy a **_Challenge Package_** from Admin
&nbsp;&nbsp;&nbsp;&nbsp; - Challenge count can be reduced with negative number <input type="checkbox" disabled>

`sc invoke <contract hash> check_challenge_package ["<alice_address>"]` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>
&nbsp;&nbsp;&nbsp;&nbsp; Businesses can **check** on the _Challenge Package_ they bought


##Claims 
`sc invoke <contract hash> promoter_claim ["<bob_address>", "<alice_address>", 'challenge-number-1']` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>
&nbsp;&nbsp;&nbsp;&nbsp; User can **claim** their funds (_~40 NODIS_) for submitting to a challenge
&nbsp;&nbsp;&nbsp;&nbsp; - can only be executed by Bob <input type="checkbox" disabled>
&nbsp;&nbsp;&nbsp;&nbsp; - can only be claimed by Bob once <input type="checkbox" disabled>
&nbsp;&nbsp;&nbsp;&nbsp; - can only claim once the submission is approved by community <input type="checkbox" disabled>

`sc invoke <contract hash> approver_claim ["<david_address>", "<bob_address>", "<alice_address>", 'challenge-number-1']` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>
&nbsp;&nbsp;&nbsp;&nbsp; User can **claim** their funds (_~ [6 / total voters] NODIS_) for approving a submission and being in the majority
&nbsp;&nbsp;&nbsp;&nbsp; - can only be executed by David <input type="checkbox" disabled>
&nbsp;&nbsp;&nbsp;&nbsp; - can only be claimed by David once <input type="checkbox" disabled>
&nbsp;&nbsp;&nbsp;&nbsp; - can only be claimed 24hr after submission was made <input type="checkbox" disabled>
&nbsp;&nbsp;&nbsp;&nbsp; - can only be claimed if approvers are in the majority <input type="checkbox" disabled>


`sc invoke <contract hash> rejecter_claim ["<francis_address>", "<clyde_address>", "<alice_address>", 'challenge-number-1']` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>
&nbsp;&nbsp;&nbsp;&nbsp; User can **claim** their funds (_~ [4 / total voters] NODIS_) for rejecting a submission and being in the majority
&nbsp;&nbsp;&nbsp;&nbsp; - can only be executed by David <input type="checkbox" disabled>
&nbsp;&nbsp;&nbsp;&nbsp; - can only be claimed by David once <input type="checkbox" disabled>
&nbsp;&nbsp;&nbsp;&nbsp; - can only be claimed 24hr after submission was made <input type="checkbox" disabled>
&nbsp;&nbsp;&nbsp;&nbsp; - can only be claimed if rejecters are in the majority <input type="checkbox" disabled>




##NODIS _GET_ Functions

###Challenge Getter

`sc invoke <smart contract> is_challenge_open ["<alice_address>", 'challenge-number-1']`
`sc invoke <smart contract> is_challenge_closed ["<alice_address>", 'challenge-number-1']`
`sc invoke <smart contract> submission_number ["<alice_address>", 'challenge-number-1']`
`sc invoke <smart contract> challenge_expiry_date ["<alice_address>", 'challenge-number-1']`

### Submission Getter

`sc invoke <smart contract> submission_approver_number ["<bob_address>", "<alice_address>", 'challenge-number-1']`
`sc invoke <smart contract> submission_rejecter_number ["<bob_address>", "<alice_address>", 'challenge-number-1']`
`sc invoke <smart contract> submission_expiry_date ["<bob_address>", "<alice_address>", 'challenge-number-1']`

### Challenge Reserve Getter

`sc invoke <smart contract> challenge_reserve []`

### Challenge Reserve Loader

`sc invoke <smart contract> load_challenge_reserve [900000000]`