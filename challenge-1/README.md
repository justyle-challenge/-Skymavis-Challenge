# Requirement
   - We can have multiple NAT Instances per AZ
   - NAT Instances may fail, resulting in AZs with fewer or no NAT Instances. 
   - If there are no NAT Instances in an AZ, the private subnets of that AZ should be allocated to egress via available NAT Instances in other AZs. 
   - If there is still at least 1 NAT Instance in an AZ, the subnets of that AZ should still be allocated to that NAT Instance which is in the same AZ
   - We try to have as close to the same number of private subnets allocated to each NAT Instance. But allocation to a NAT Instance in the same AZ takes priority.

# Example usage
```
nat_instances = [
    NATInstance(1, "us-west1-a"),
    NATInstance(2, "us-west1-b"),
    NATInstance(3, "us-west1-b"),
]

subnets = [
    Subnet(1, "us-west1-a"),
    Subnet(2, "us-west1-b"),
    Subnet(3, "us-west1-b"),
    Subnet(4, "us-west1-c"),
]
```

# Run no weight
```shell
pỵthon app.py
```

Result:
```
NAT Instance 1 (us-west1-a): Subnet 1 (us-west1-a), Subnet 4 (us-west1-c)
NAT Instance 2 (us-west1-b): Subnet 2 (us-west1-b)
NAT Instance 3 (us-west1-b): Subnet 3 (us-west1-b)
```

# Bonus (with weight)
   - What if each Subnet has a `Weight int32` attribute and we try to make total weight allocated to each NAT Instance the same no matter how subnets allocated to each NAT Instance?
```shell
pỵthon app-weight.py
```

Result:
```
NAT Instance 1 (us-west1-a): Subnet 1 (us-west1-a) - Weight 3 ===> Total Weight: 3
NAT Instance 2 (us-west1-b): Subnet 2 (us-west1-b) - Weight 2 ===> Total Weight: 2
NAT Instance 3 (us-west1-b): Subnet 3 (us-west1-b) - Weight 1, Subnet 4 (us-west1-c) - Weight 4 ===> Total Weight: 5
```