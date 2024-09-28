from collections import defaultdict
import unittest

class NATInstance:
    def __init__(self, id, az):
        self.id = id
        self.az = az
        self.subnets = []
        self.total_weight = 0  # Track the total weight allocated to this NAT

    def __repr__(self):
        subnets_str = ', '.join([f"Subnet {s.id} ({s.az}) - Weight {s.weight}" for s in self.subnets])
        return f"NAT Instance {self.id} ({self.az}): {subnets_str} ===> Total Weight: {self.total_weight}"

class Subnet:
    def __init__(self, id, az, weight=1):
        self.id = id
        self.az = az
        self.weight = weight

    def __repr__(self):
        return f"Subnet {self.id} ({self.az}, Weight: {self.weight})"

def allocate_subnets_to_nat_instances(subnets, nat_instances):
    # Group NAT instances by AZ
    nat_by_az = defaultdict(list)
    for nat in nat_instances:
        nat_by_az[nat.az].append(nat)

    # Group subnets by AZ
    subnets_by_az = defaultdict(list)
    for subnet in subnets:
        subnets_by_az[subnet.az].append(subnet)

    # Unallocated subnets
    unallocated_subnets = []

    # Allocate subnets to NAT instances in the same AZ with weight balancing
    for az, az_subnets in subnets_by_az.items():
        az_nats = nat_by_az.get(az, [])
        if az_nats:
            # Sort by least total weight NAT instance
            az_nats.sort(key=lambda nat: nat.total_weight)
            for subnet in az_subnets:
                # Allocate the subnet to the NAT instance with the least total weight
                nat = az_nats[0]
                nat.subnets.append(subnet)
                nat.total_weight += subnet.weight
                az_nats.sort(key=lambda nat: nat.total_weight)  # Re-sort after adding the subnet
        else:
            # No NAT instance in this AZ, subnets need to be allocated elsewhere
            unallocated_subnets.extend(az_subnets)

    # Allocate unallocated subnets to NAT instances in other AZs (cross-AZ)
    all_nats = sorted(nat_instances, key=lambda nat: nat.total_weight)  # Sort by least total weight
    for subnet in unallocated_subnets:
        nat = all_nats[0]
        nat.subnets.append(subnet)
        nat.total_weight += subnet.weight
        all_nats.sort(key=lambda nat: nat.total_weight)  # Re-sort after adding the subnet

# Problems
nat_instances = [
    NATInstance(1, "us-west1-a"),
    NATInstance(2, "us-west1-b"),
    NATInstance(3, "us-west1-b"),
]

subnets = [
    Subnet(1, "us-west1-a", weight=3),
    Subnet(2, "us-west1-b", weight=2),
    Subnet(3, "us-west1-b", weight=1),
    Subnet(4, "us-west1-c", weight=4),  # Cross-AZ allocation needed
]

allocate_subnets_to_nat_instances(subnets, nat_instances)

print("### The result ###")
for nat in nat_instances:
    print(nat)

# Unit test
print("### The unit test result ###")
class TestSubnetAllocationWithWeight(unittest.TestCase):

    def test_allocate_subnets_same_az(self):
        nat_instances = [
            NATInstance(1, "us-west1-a"),
            NATInstance(2, "us-west1-b"),
            NATInstance(3, "us-west1-b"),
        ]
        subnets = [
            Subnet(1, "us-west1-a", 3),
            Subnet(2, "us-west1-b", 2),
            Subnet(3, "us-west1-b", 1),
        ]
        
        allocate_subnets_to_nat_instances(subnets, nat_instances)
        
        # Check that subnets are allocated within the same AZ
        self.assertEqual(nat_instances[0].total_weight, 3)
        self.assertEqual(nat_instances[1].total_weight, 2)
        self.assertEqual(nat_instances[2].total_weight, 1)
        
        # Ensure Subnet 1 is allocated to NAT 1 (same AZ)
        self.assertIn(subnets[0], nat_instances[0].subnets)
        # Ensure Subnet 2 is allocated to NAT 2 (same AZ)
        self.assertIn(subnets[1], nat_instances[1].subnets)
        # Ensure Subnet 3 is allocated to NAT 3 (same AZ)
        self.assertIn(subnets[2], nat_instances[2].subnets)

        print("--- Test allocating subnets same AZ with Weight ---")
        for nat in nat_instances:
            print(nat)

    def test_allocate_subnets_cross_az(self):
        nat_instances = [
            NATInstance(1, "us-west1-a"),
            NATInstance(2, "us-west1-b"),
        ]
        subnets = [
            Subnet(1, "us-west1-a", 3),
            Subnet(2, "us-west1-b", 2),
            Subnet(3, "us-west1-c", 5),  # No NAT in "us-west1-c", should be cross-AZ allocated
        ]
        
        allocate_subnets_to_nat_instances(subnets, nat_instances)
        
        # Check that subnets are allocated correctly and the total weight is balanced
        total_weights = [nat.total_weight for nat in nat_instances]
        self.assertEqual(sum(total_weights), 10)
        self.assertAlmostEqual(nat_instances[0].total_weight, 3)  # NAT 1 should get Subnet 1 (3)
        self.assertEqual(nat_instances[1].total_weight, 7)  # NAT 2 should have Subnet 2 (2) + Subnet 3 (5)

        print("--- Test allocating subnets cross AZ with Weight ---")
        for nat in nat_instances:
            print(nat)

    def test_allocate_subnets_no_nat_in_az(self):
        nat_instances = [
            NATInstance(1, "us-west1-a"),
            NATInstance(2, "us-west1-b"),
        ]
        subnets = [
            Subnet(1, "us-west1-a", 3),
            Subnet(2, "us-west1-c", 4),  # No NAT in "us-west1-c", should be cross-AZ allocated
        ]
        
        allocate_subnets_to_nat_instances(subnets, nat_instances)
        
        # Check that subnets in unavailable AZ (us-west1-c) are allocated to other AZs
        total_weights = [nat.total_weight for nat in nat_instances]
        self.assertEqual(sum(total_weights), 7)
        self.assertAlmostEqual(nat_instances[0].total_weight, 3)  # NAT 1 should get Subnet 1 (3)
        self.assertEqual(nat_instances[1].total_weight, 4)  # NAT 2 should have Subnet 2 (4)

        print("--- Test allocating subnets no nat in AZ with Weight ---")
        for nat in nat_instances:
            print(nat)

    def test_balanced_weight_distribution(self):
        nat_instances = [
            NATInstance(1, "us-west1-a"),
            NATInstance(2, "us-west1-b"),
        ]
        subnets = [
            Subnet(1, "us-west1-a", 5),
            Subnet(2, "us-west1-b", 2),
            Subnet(3, "us-west1-c", 3),  # No NAT in "us-west1-c", should be cross-AZ allocated
        ]
        
        allocate_subnets_to_nat_instances(subnets, nat_instances)
        
        # Ensure the total weight is balanced between NAT instances
        total_weights = [nat.total_weight for nat in nat_instances]
        self.assertEqual(sum(total_weights), 10)
        # NAT 1 should have Subnet 1 (5)
        self.assertEqual(nat_instances[0].total_weight, 5)
        # NAT 2 should have Subnet 2 (2) + Subnet 3 (3)
        self.assertEqual(nat_instances[1].total_weight, 5)

        print("--- Test balancing number of subnets with Weight ---")
        for nat in nat_instances:
            print(nat)

if __name__ == '__main__':
    unittest.main()
