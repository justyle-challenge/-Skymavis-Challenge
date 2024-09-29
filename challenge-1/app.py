from collections import defaultdict
import unittest

class NATInstance:
    def __init__(self, id, az):
        self.id = id
        self.az = az
        self.subnets = []

    def __repr__(self):
        subnets_str = ', '.join([f"Subnet {s.id} ({s.az})" for s in self.subnets])
        return f"NAT Instance {self.id} ({self.az}): {subnets_str}"

class Subnet:
    def __init__(self, id, az, priority=1):
        self.id = id
        self.az = az
        self.priority = priority

    def __repr__(self):
        return f"Subnet {self.id} ({self.az})"

def allocate_subnets_to_nat_instances(subnets, nat_instances):
    # Group NAT instances by AZ
    nat_by_az = defaultdict(list)
    for nat in nat_instances:
        nat_by_az[nat.az].append(nat)

    # print(f"Group NAT instances by AZ:\n",nat_by_az)

    # Group subnets by AZ
    subnets_by_az = defaultdict(list)
    for subnet in subnets:
        subnets_by_az[subnet.az].append(subnet)

    # # Allocate subnets to NAT instances in the same AZ with priority (bonus)
    # for az, az_subnets in subnets_by_az.items():
    #     az_subnets.sort(key=lambda subnet: subnet.priority, reverse=True) # Sort subnets by priority descending
    
    # print (f"Group Subnets by AZ:\n", subnets_by_az)

    # Unallocated subnets
    unallocated_subnets = []

    # Allocate subnets to NAT instances in the same AZ
    for az, az_subnets in subnets_by_az.items():
        az_nats = nat_by_az.get(az, [])
        if az_nats:
            # Distribute subnets evenly across NAT instances in the same AZ
            az_nats.sort(key=lambda nat: len(nat.subnets))  # Sort by least-loaded NAT instance based on the number of subnets
            for i, subnet in enumerate(az_subnets):     # Assigns each subnet to a NAT instance with round-robin
                nat = az_nats[i % len(az_nats)]
                nat.subnets.append(subnet)
        else:
            # No NAT instance in this AZ, subnets need to be allocated elsewhere
            unallocated_subnets.extend(az_subnets)

    # Allocate unallocated subnets to NAT instances in other AZs
    all_nats = sorted(nat_instances, key=lambda nat: len(nat.subnets))
    for i, subnet in enumerate(unallocated_subnets):
        nat = all_nats[i % len(all_nats)]
        nat.subnets.append(subnet)

# Problems
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

print("### Problems ###\n" + "--- NAT Instances ---\n" + "\n".join([f"NAT Instance {nat.id} ({nat.az})" for nat in nat_instances]) +
      "\n--- Subnets ---\n" + "\n".join([f"Subnet {subnet.id} ({subnet.az})" for subnet in subnets]))

allocate_subnets_to_nat_instances(subnets, nat_instances)

print("\n### The result ###")
for nat in nat_instances:
    print(nat)

# Unit test
print("\n### The unit test result ###")
class TestSubnetAllocationWithoutWeight(unittest.TestCase):

    def test_allocate_subnets_same_az(self):
        nat_instances = [
            NATInstance(1, "us-west1-a"),
            NATInstance(2, "us-west1-b"),
            NATInstance(3, "us-west1-b"),
        ]
        subnets = [
            Subnet(1, "us-west1-a"),
            Subnet(2, "us-west1-b"),
            Subnet(3, "us-west1-b"),
        ]
        
        allocate_subnets_to_nat_instances(subnets, nat_instances)
        
        # Check that subnets are allocated within the same AZ
        self.assertEqual(len(nat_instances[0].subnets), 1)
        self.assertEqual(len(nat_instances[1].subnets), 1)
        self.assertEqual(len(nat_instances[2].subnets), 1)
        
        # Ensure Subnet 1 is allocated to NAT 1 (same AZ)
        self.assertIn(subnets[0], nat_instances[0].subnets)
        # Ensure Subnet 2 is allocated to NAT 2 (same AZ)
        self.assertIn(subnets[1], nat_instances[1].subnets)
        # Ensure Subnet 3 is allocated to NAT 3 (same AZ)
        self.assertIn(subnets[2], nat_instances[2].subnets)

        print("--- Test allocating subnets same AZ ---")
        for nat in nat_instances:
            print(nat)

    def test_allocate_subnets_cross_az(self):
        nat_instances = [
            NATInstance(1, "us-west1-a"),
            NATInstance(2, "us-west1-b"),
        ]
        subnets = [
            Subnet(1, "us-west1-a"),
            Subnet(2, "us-west1-b"),
            Subnet(3, "us-west1-c"),  # No NAT in "us-west1-c", should be cross-AZ allocated
        ]
        
        allocate_subnets_to_nat_instances(subnets, nat_instances)
        
        # Subnet 3 should be allocated cross-AZ
        self.assertEqual(len(nat_instances[0].subnets), 2)  # NAT 1 should have 2 subnets
        self.assertEqual(len(nat_instances[1].subnets), 1)  # NAT 2 should have 1 subnet

        print("--- Test allocating subnets cross AZ ---")
        for nat in nat_instances:
            print(nat)

    def test_allocate_subnets_no_nat_in_az(self):
        nat_instances = [
            NATInstance(1, "us-west1-a"),
            NATInstance(2, "us-west1-b"),
        ]
        subnets = [
            Subnet(1, "us-west1-a"),
            Subnet(2, "us-west1-c"),  # No NAT in "us-west1-c", should be cross-AZ allocated
        ]
        
        allocate_subnets_to_nat_instances(subnets, nat_instances)
        
        # Check that subnets in unavailable AZ (us-west1-c) are allocated to other AZs
        self.assertEqual(len(nat_instances[0].subnets), 1)  # NAT 1 should have 1 subnet
        self.assertEqual(len(nat_instances[1].subnets), 1)  # NAT 2 should have 1 subnet

        print("--- Test allocating subnets no nat in AZ ---")
        for nat in nat_instances:
            print(nat)

    def test_balanced_number_of_subnets(self):
        nat_instances = [
            NATInstance(1, "us-west1-a"),
            NATInstance(2, "us-west1-b"),
        ]
        subnets = [
            Subnet(1, "us-west1-a"),
            Subnet(2, "us-west1-a"),
            Subnet(3, "us-west1-c"),  # No NAT in "us-west1-c", should be cross-AZ allocated
        ]
        
        allocate_subnets_to_nat_instances(subnets, nat_instances)
        
        # Check if subnets are evenly distributed across NAT instances
        self.assertEqual(len(nat_instances[0].subnets), 2)  # NAT 1 should have 2 subnets
        self.assertEqual(len(nat_instances[1].subnets), 1)  # NAT 2 should have 1 subnet

        print("--- Test balancing number of subnets ---")
        for nat in nat_instances:
            print(nat)

if __name__ == '__main__':
    unittest.main()
