module "team1_membership" {
  source   = "./module/team_membership"
  team_name = local.team1_name
  team_members   = local.team1_members

}

module "team2_membership" {
  source   = "./module/team_membership"
  team_name = local.team2_name
  team_members   = local.team2_members
}

module "team3_membership" {
  source   = "./module/team_membership"
  team_name = local.team3_name
  team_members   = local.team3_members
}

module "team4_membership" {
  source   = "./module/team_membership"
  team_name = local.team4_name
  team_members   = local.team4_members
}

module "team5_membership" {
  source   = "./module/team_membership"
  team_name = local.team5_name
  team_members   = local.team5_members
}

module "team6_membership" {
  source   = "./module/team_membership"
  team_name = local.team6_name
  team_members   = local.team6_members
}