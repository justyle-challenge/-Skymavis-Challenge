# module/team_membership/team_membership.tf
variable "team_name" {
  type = string
}

variable "team_members" {
  type = list(object({
    username = string
    role     = string
  }))
}

resource "github_team_membership" "membership" {
  for_each = { for member in var.team_members : member.username => member }

  team_id  = github_team.team.id
  username = each.value.username
  role     = each.value.role
}

resource "github_team" "team" {
  name = var.team_name
}
