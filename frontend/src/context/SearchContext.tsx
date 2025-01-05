import React, { createContext, useContext, useState } from "react";

interface SearchContextType {
  selectedTeams: string[];
  toggleTeamSelection: (team: string) => void;
  selectedTournaments: string[];
  setTournamentSelection: (tournament: string, isChecked: boolean) => void;
  teamType: string;
  setTeamType: (type: string) => void;
}

const SearchContext = createContext<SearchContextType | undefined>(undefined);

export const SearchProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [selectedTeams, setSelectedTeams] = useState<string[]>([]);
  const [selectedTournaments, setSelectedTournaments] = useState<string[]>([]);
  const [teamType, setTeamType] = useState<string>("both"); // 默认值为 "both"

  const toggleTeamSelection = (team: string) => {
    setSelectedTeams((prev) =>
      prev.includes(team) ? prev.filter((t) => t !== team) : [...prev, team]
    );
  };

  const setTournamentSelection = (tournament: string, isChecked: boolean) => {
    setSelectedTournaments((prev) =>
      isChecked ? [...prev, tournament] : prev.filter((t) => t !== tournament)
    );
  };

  return (
    <SearchContext.Provider
      value={{
        selectedTeams,
        toggleTeamSelection,
        selectedTournaments,
        setTournamentSelection,
        teamType,
        setTeamType,
      }}
    >
      {children}
    </SearchContext.Provider>
  );
};

export const useSearch = (): SearchContextType => {
  const context = useContext(SearchContext);
  if (!context) {
    throw new Error("useSearch must be used within a SearchProvider");
  }
  return context;
};
