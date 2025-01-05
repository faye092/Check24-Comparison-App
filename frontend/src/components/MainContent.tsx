import React, { useEffect, useState } from "react";
import { Box, Text, Spinner, VStack, Button } from "@chakra-ui/react";
import { Collapsible } from "@chakra-ui/react";
import { useSearch } from "../context/SearchContext";
import api from "../services/api";
import { Game, FetchResponse } from "../types"; // 导入类型

const MainContent: React.FC = () => {
  const { selectedTeams, selectedTournaments, teamType } = useSearch(); // 获取用户选择的球队、联赛和比赛类型
  const [gamesByTournament, setGamesByTournament] = useState<Record<string, Game[]>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchGames = async () => {
      setLoading(true);
      setError(null);

      try {
        let response;

        if (selectedTeams.length > 0 && selectedTournaments.length === 0) {
          // 仅选择了球队
          response = await api.get<FetchResponse<Game[]>>("/games/team", {
            params: {
              team_name: selectedTeams.join(","),
              team_type: teamType,
              page: 1,
              per_page: 50,
            },
          });
        } else if (selectedTeams.length === 0 && selectedTournaments.length > 0) {
          // 仅选择了联赛
          response = await api.get<FetchResponse<Game[]>>("/games/tournament", {
            params: {
              tournament_name: selectedTournaments.join(","),
              page: 1,
              per_page: 50,
            },
          });
        } else if (selectedTeams.length > 0 && selectedTournaments.length > 0) {
          // 同时选择了球队和联赛
          response = await api.get<FetchResponse<Game[]>>("/games/team-and-tournament", {
            params: {
              team_name: selectedTeams.join(","),
              tournament_name: selectedTournaments.join(","),
              team_type: teamType,
              page: 1,
              per_page: 50,
            },
          });
        } else {
          // 未选择任何条件
          setGamesByTournament({});
          setLoading(false);
          return;
        }

        // 处理后端返回的数据
        const games = response.data.data;

        // 按联赛分组比赛
        const groupedGames = games.reduce((acc: Record<string, Game[]>, game: Game) => {
          if (!acc[game.tournament_name]) {
            acc[game.tournament_name] = [];
          }
          acc[game.tournament_name].push(game);
          return acc;
        }, {});

        setGamesByTournament(groupedGames);
      } catch (err) {
        console.error("Error fetching games:", err);
        setError(err instanceof Error ? err.message : "An error occurred while fetching games.");
      } finally {
        setLoading(false);
      }
    };

    fetchGames();
  }, [selectedTeams, selectedTournaments, teamType]);

  return (
    <Box>
      {loading && <Spinner />}
      {error && (
        <Text color="red.500" my={4}>
          {error}
        </Text>
      )}
      {!loading && Object.keys(gamesByTournament).length === 0 && (
        <Text>
          {selectedTeams.length > 0 && selectedTournaments.length === 0
            ? "No games found for the selected team(s)."
            : selectedTeams.length === 0 && selectedTournaments.length > 0
            ? "No games found for the selected tournament(s)."
            : "No games found for the selected criteria."}
        </Text>
      )}
      {!loading &&
        Object.keys(gamesByTournament).map((tournament) => (
          <Box key={tournament} mb={2}> {/* 增加每个联赛之间的间隙 */}
            <Collapsible.Root>
              <Collapsible.Trigger>
                <Button
                  size="md"
                  variant="ghost"
                  fontWeight="bold" // 字体加重
                  bg="gray.100" // 默认背景颜色
                  _hover={{ bg: "gray.200" }} // 鼠标悬停时背景颜色
                  _active={{ bg: "#0273C3", color: "white" }} // 点击时背景颜色和字体颜色
                  textAlign="left"
                  w="100%" // 按钮宽度填满
                >
                  {tournament}
                </Button>
              </Collapsible.Trigger>
              <Collapsible.Content>
                <VStack align="start" mt={2} p={2}>
                  {gamesByTournament[tournament].length > 0 ? (
                    gamesByTournament[tournament].map((game) => (
                      <Box
                        key={game.id}
                        p={4}
                        mb={1}
                        border="1px solid #e2e8f0"
                        borderRadius="md"
                        w="100%"
                        fontSize="sm" // 比赛字体较小
                        _hover={{ bg: "gray.50" }} // 鼠标悬停比赛卡片时的背景颜色
                      >
                        <Text>{`${game.team_home} - ${game.team_away}`}</Text>
                        <Text color="gray.600" fontSize="xs">
                          {new Date(game.starts_at).toLocaleString(undefined, {
                            weekday: "short",
                            year: "numeric",
                            month: "short",
                            day: "numeric",
                            hour: "2-digit",
                            minute: "2-digit",
                          })}
                        </Text>
                      </Box>
                    ))
                  ) : (
                    <Text>No games available for this tournament.</Text>
                  )}
                </VStack>
              </Collapsible.Content>
            </Collapsible.Root>
          </Box>
        ))}
    </Box>
  );
};

export default MainContent;
