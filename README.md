# DevOps Challenge

Please solve three challenges presented below

1. You have 3 Availability Zones (AZs) with n Private Subnets, and m NAT Instances per AZ. Private Subnets need to route traffic through NAT Instances which block any traffic not going to a whitelisted domain. 
   For HA we have to dynamically allocate private subnets to NAT Instances. First of all, we need to allocate subnets to NAT Instances within the same AZ. If there are no healthy NAT Instances in the same AZ, only then will we allocate subnets to any NAT Instance in any other AZ.

   - We can have multiple NAT Instances per AZ
   - NAT Instances may fail, resulting in AZs with fewer or no NAT Instances. 
   - If there are no NAT Instances in an AZ, the private subnets of that AZ should be allocated to egress via available NAT Instances in other AZs. 
   - If there is still at least 1 NAT Instance in an AZ, the subnets of that AZ should still be allocated to that NAT Instance which is in the same AZ
   - We try to have as close to the same number of private subnets allocated to each NAT Instance. But allocation to a NAT Instance in the same AZ takes priority.
   
   If you use Golang, you can use the following playground to implement function
   
   https://play.golang.org/p/zYJ-bf_MDBg
   
   Possible problem and solution:
   
   ```
   # problem
   NATInstances:
     1 - us-west1-a
     2 - us-west1-b
     3 - us-west1-b
   
   Subnets:
     1 - us-west1-a
     2 - us-west1-b
     3 - us-west1-b
     4 - us-west1-c
   
   # solution
   Instance (1 - us-west1-a):
	subnet (1 - us-west1-a)
	subnet (4 - us-west1-c)
   Instance (2 - us-west1-b):
	subnet (2 - us-west1-b)
   Instance (3 - us-west1-b):
	subnet (3 - us-west1-b)

   ```
   
   If you use golang, please send a link to the Go Playground to run/test your solution, or you may create a git repository, implement a more complete program including Unit Tests for several edge cases you can think of (no NAT Instances, no Subnets, ...)
   
   If you use python / bash / ... please provide link to git repository. Ensure it is easy to pull/run your solution.

   Bonus: What if each Subnet has a `Weight int32` attribute and we try to make total weight allocated to each NAT Instance the same no matter how subnets allocated to each NAT Instance?

1. Write an application [http sd exporter](https://prometheus.io/docs/prometheus/latest/http_sd/). 

    Your application needs write blackbox exporter check the difference in block number between two providers Ankr and Infura.:
    -   if Ankr blocknumber - Infura blocknumber < 5 => success
    -   else => fail

    We're assuming that Infrura is the trusted source for checking the block number.

    Note: Infura for sign up free account and docs https://www.ankr.com/rpc/eth/ and https://docs.infura.io/

    Example: Get blocknumber with curl
    ```
    curl https://mainnet.infura.io/v3/ID
    -X POST \
    -H "Content-Type: application/json" 
    -d '{ 
     "jsonrpc": "2.0", 
     "method": eth_blockNumber, 
     "params": [], 
     "id": 1, 
    }'
    ```
    Please submit a link to a public GitHub repository with the source code of your solution. As an alternative, you may send a tar archive by email, but this is discouraged.

1. Write a terraform configuration to manage GitHub teams - with the following Role matrix.

   Empty spaces represent the user is not a member of the team

   | Username | Team1 | Team2 | Team3 | Team4 | Team5 | Team6 |
   |----------|-------|-------|-------|-------|-------|-------|
   |User1 | member | maintainer | member | member | maintainer | member |
   |User2 | maintainer | member	| member | maintainer	| member | member |
   |User3 | member | member | maintainer | member | member | member |
   |User4 |  | member | member | member | member | maintainer | 
   |User5 | member |  | member | member |  | member | 
   |User6 | member | member | member | member | member |  |
   |User7 | member | member | member | member | member | member |
   |User8 | member | member |  | member | member | member |
   |User9 | member | member |  | member | member | member |
   |User10 | member | member |  | member | member | member |
   
   Take into consideration ease of maintenance 
