variable "project" {
  description = "The name of the project"
  default = "challenge"
}

locals {
    # Team 1
    team1_name = "Team1"
    team1_members = [
      { username = "User1", role = "member" },
      { username = "User2", role = "maintainer" },
      { username = "User3", role = "member" },
      { username = "User5", role = "member" },
      { username = "User6", role = "member" },
      { username = "User7", role = "member" },
      { username = "User8", role = "member" },
      { username = "User9", role = "member" },
      { username = "User10", role = "member" }
    ]

    # Team 2
    team2_name = "Team2"
    team2_members = [
      { username = "User1", role = "maintainer" },
      { username = "User2", role = "member" },
      { username = "User3", role = "member" },
      { username = "User4", role = "member" },
      { username = "User6", role = "member" },
      { username = "User7", role = "member" },
      { username = "User8", role = "member" },
      { username = "User9", role = "member" },
      { username = "User10", role = "member" }
    ]

    # Team 3
    team3_name = "Team3"
    team3_members = [
      { username = "User1", role = "member" },
      { username = "User2", role = "member" },
      { username = "User3", role = "maintainer" },
      { username = "User4", role = "member" },
      { username = "User5", role = "member" },
      { username = "User6", role = "member" },
      { username = "User7", role = "member" }
    ]

    # Team 4
    team4_name = "Team4"
    team4_members = [
      { username = "User1", role = "member" },
      { username = "User2", role = "maintainer" },
      { username = "User3", role = "member" },
      { username = "User4", role = "member" },
      { username = "User5", role = "member" },
      { username = "User6", role = "member" },
      { username = "User7", role = "member" },
      { username = "User8", role = "member" },
      { username = "User9", role = "member" },
      { username = "User10", role = "member" }
    ]

    # Team 5
    team5_name = "Team5"
    team5_members = [
      { username = "User1", role = "maintainer" },
      { username = "User2", role = "member" },
      { username = "User3", role = "member" },
      { username = "User4", role = "member" },
      { username = "User6", role = "member" },
      { username = "User7", role = "member" },
      { username = "User8", role = "member" },
      { username = "User9", role = "member" },
      { username = "User10", role = "member" }
    ]

    # Team 6
    team6_name = "Team6"
    team6_members = [
      { username = "User1", role = "member" },
      { username = "User2", role = "member" },
      { username = "User3", role = "member" },
      { username = "User4", role = "maintainer" },
      { username = "User5", role = "member" },
      { username = "User7", role = "member" },
      { username = "User8", role = "member" },
      { username = "User9", role = "member" },
      { username = "User10", role = "member" }
    ]

}
