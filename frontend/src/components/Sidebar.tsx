import React from "react";
import { Box, VStack, Heading, Text, HStack } from "@chakra-ui/react";
import { useSearch } from "../context/SearchContext";

const Sidebar: React.FC = () => {
  const { selectedTeams, toggleTeamSelection, selectedTournaments, setTournamentSelection, teamType, setTeamType } = useSearch();
  
  const tournamentCategories = [
    {
      name: "INTERNATIONAL",
      icon: "🌍",
      tournaments: ["Europameisterschaft 2024"],
    },
    {
      name: "EUROPEAN ELITE COMPETITIONS",
      icon: "⭐",
      tournaments: [
        "UEFA Champions League 24/25",
        "UEFA Europa League 24/25",
        "UEFA Conference League 24/25",
        "UEFA Super Cup 2024",
      ],
    },
    {
      name: "TOP 5 LEAGUES",
      icon: "🏆",
      tournaments: [
        "Bundesliga 23/24",
        "Bundesliga 24/25",
        "Premier League 24/25",
        "LaLiga 24/25",
        "Serie A 23/24",
        "Serie A 24/25",
        "Ligue 1 24/25",
      ],
    },
    {
      name: "MAJOR DOMESTIC CUPS",
      icon: "🏆",
      tournaments: [
        "DFB-Pokal 24/25",
        "FA Cup 23/24",
        "EFL Cup 23/24",
        "EFL Cup 24/25",
        "Copa del Rey 23/24",
        "Copa del Rey 24/25",
        "Coppa Italia 23/24",
        "Coppa Italia 24/25",
        "Coupe de France 23/24",
      ],
    },
    {
      name: "SECONDARY LEAGUES",
      icon: "⚪",
      tournaments: [
        "2. Bundesliga 23/24",
        "2. Bundesliga 24/25",
        "3. Liga 23/24",
        "3. Liga 24/25",
        "Bundesliga AUT 23/24",
        "Bundesliga AUT 24/25",
        "Süper Lig 23/24",
        "Süper Lig 24/25",
        "Liga Portugal 23/24",
        "Liga Portugal 24/25",
        "Eredivisie 24/25",
        "Saudi Prof. League 23/24",
        "Saudi Prof. League 24/25",
        "Major League Soccer 2024",
      ],
    },
    {
      name: "DOMESTIC SUPER CUPS",
      icon: "⭐",
      tournaments: [
        "Supercup 2024",
        "Community Shield 2024",
        "Trophée des Champions 2024",
      ],
    },
  ];

  const popularTeams = [
    "Bayern München",
    "Real Madrid",
    "AS Rom",
    "Los Angeles FC",
    "Oxford United",
    "Hatayspor",
    "Deutschland",
    "Manchester City",
    "Paris Saint-Germain",
    "Borussia Dortmund",
  ];

  return (
    <Box
      as="aside"
      w="300px"
      minH="0"
      bg="gray.50"
      borderRight="1px solid #e2e8f0"
      overflowY="auto"
      p={1}
      pt={0}
      mt={0}
    >
      <VStack align="start" p={2}>
        {/* Team Type Filter */}
        <Box>
          <HStack align="center" mb={2}>
            <Text fontSize="lg" color="blue.500">
              📊
            </Text>
            <Heading size="md" color="gray.700">
              TEAM TYPE
            </Heading>
          </HStack>
          <VStack align="start" p={2}>
            {["both", "home", "away"].map((type) => (
              <label
                key={type}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                }}
              >
                <input
                  type="radio"
                  name="teamType"
                  value={type}
                  checked={teamType === type}
                  onChange={() => setTeamType(type)}
                />
                <Text fontSize="xs" color="gray.800">
                  {type === "both"
                    ? "All"
                    : type === "home"
                    ? "Home"
                    : "Away"}
                </Text>
              </label>
            ))}
          </VStack>
        </Box>

        {/* Popular Teams Section */}
        <Box>
          <HStack align="center" mb={2}>
            <Text fontSize="lg" color="blue.500">
              ⚽
            </Text>
            <Heading size="md" color="gray.700">
              POPULAR TEAMS
            </Heading>
          </HStack>
          <HStack wrap="wrap" p={2} align="start">
            {popularTeams.map((team) => (
              <Box
                key={team}
                bg={selectedTeams.includes(team) ? "#0273C3" : "gray.200"}
                color={selectedTeams.includes(team) ? "white" : "gray.800"}
                px={3}
                py={1}
                borderRadius="xl"
                cursor="pointer"
                _hover={{
                  bg: selectedTeams.includes(team) ? "#025a93" : "gray.300",
                }}
                onClick={() => toggleTeamSelection(team)}
              >
                <Text fontSize="xs">{team}</Text>
              </Box>
            ))}
          </HStack>
        </Box>

        {/* Tournament Categories Section */}
        {tournamentCategories.map((category) => (
          <Box key={category.name}>
            <HStack mb={2}>
              <Text fontSize="lg" color="blue.500">
                {category.icon}
              </Text>
              <Heading size="md" color="gray.700">
                {category.name}
              </Heading>
            </HStack>
            <VStack align="start" p={2}>
                {category.tournaments.map((tournament) => (
                    <label
                    key={tournament}
                    style={{ display: "flex", alignItems: "center", gap: "8px" }}
                    >
                    <input
                      type="checkbox"
                      name={tournament}
                      checked={selectedTournaments.includes(tournament)}
                      onChange={(e) => setTournamentSelection(tournament, e.target.checked)}
                    />
                    <Text fontSize="xs" color="gray.800">
                        {tournament}
                    </Text>
                    </label>
                ))}
            </VStack>
          </Box>
        ))}
      </VStack>
    </Box>
  );
};

export default Sidebar;
