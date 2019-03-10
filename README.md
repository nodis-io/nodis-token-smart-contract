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

`sc invoke <contract hash> mintTokens [] --attach-gas={number}` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>

##Transferring NODIS tokens

`sc invoke <contract address> transfer ["<owner address>", "<destination address>", 500]` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>

##Mining Rate

`sc invoke <contract hash> get_mining_rate []` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>

`sc invoke <contract hash> get_promoter_mining_rate []` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>

`sc invoke <contract hash> get_approver_mining_rate [1]` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>

`sc invoke <contract hash> get_rejecter_mining_rate [1]` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>

`sc invoke <contract address> transfer ["<admin address>", "b'CHALLENGE_SYSTEM_RESERVE'", 500]` <span style="color:BlueViolet;border-color:BlueViolet;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">ADMIN</span>


##Challenge System 

`sc invoke <contract address> register_business ["<business address>"]` <span style="color:BlueViolet;border-color:BlueViolet;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">ADMIN</span>

`sc invoke <contract address> signout_business ["<business address>"]` <span style="color:BlueViolet;border-color:BlueViolet;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">ADMIN</span>

`sc invoke <contract address> create_challenge ["<Alice's address>", 'challenge-number-1']` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span> <span style="color:DarkSlateGrey;border-color:DarkSlateGrey;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">BUSINESS</span>

`sc invoke <contract address> submit ["<Bob's address>", "<Alice's address>", 'challenge-number-1']` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>

`sc invoke <contract address> approve_submission ["<David's address>", "<Bob's address>", "<Alice's address>", 'challenge-number-1']` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>

`sc invoke <contract address> reject_submission ["<Francis' address>", "<Bob's address>", "<Alice's address>", 'challenge-number-1']` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>

`sc invoke <contract address> close_challenge ["<Alice's address>", 'challenge-number-1']` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span> <span style="color:DarkSlateGrey;border-color:DarkSlateGrey;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">BUSINESS</span>


##Challenge Package

`sc invoke <contract hash> buy_challenge_package ["<alice_address>", 2]` <span style="color:BlueViolet;border-color:BlueViolet;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">ADMIN</span> <span style="color:DarkSlateGrey;border-color:DarkSlateGrey;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">BUSINESS</span>

`sc invoke <contract hash> check_challenge_package ["<alice_address>"]` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>


##Claims 
`sc invoke <contract hash> promoter_claim ["<bob_address>", "<alice_address>", 'challenge-number-1']` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>

`sc invoke <contract hash> approver_claim ["<david_address>", "<bob_address>", "<alice_address>", 'challenge-number-1']` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>


`sc invoke <contract hash> rejecter_claim ["<francis_address>", "<clyde_address>", "<alice_address>", 'challenge-number-1']` <span style="color:green;border-color:green;border-style:solid;border-width:1px;border-radius:25px;font-size:10px;">PUBLIC</span>


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

# Audit

This contract was audited by Red4Sec CyberSecurity S.L.

<p align="center">
  <img
    src="https://red4sec.com/en"
    width="125px;">
<p align="center"><a href="https://red4sec.com/en">Website</a></p>
    
</p>
