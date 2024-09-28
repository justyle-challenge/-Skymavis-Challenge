# Requirement
   - Write a terraform configuration to manage GitHub teams - with the following Role matrix.
   - Empty spaces represent the user is not a member of the team

Take into consideration ease of maintenance  -> we should use modular to easy to maintain

# Apply
```shell
terraform init
terraform plan --out terraform.out
terraform apply "terraform.out"
```

# Note
User1 -> User10 (need to replace) should be part of the organization. Invite the user first, ensure they accept the invite.