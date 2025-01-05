import React from "react";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import NavControls from "./components/NavControls";
import MainContent from "./components/MainContent";
import { Box, Flex } from "@chakra-ui/react";
import { SearchProvider } from "./context/SearchContext";

const App: React.FC = () => {
  return (
    <SearchProvider>
      <Box minH="100vh" bg="gray.50">
        {/* Top Nav */}
        <Navbar
          onSearch={(query: string) => console.log("Search query:", query)}
        />

        {/* Nav Controls */}
        <NavControls />

        {/* Main Layout */}
        <Flex flex="1" bg="gray.50">
          {/* sidebar */}
          <Sidebar />

          {/* Main Content Area*/}
          <Box flex="1" p="4">
            <MainContent />
          </Box>
        </Flex>
      </Box>
    </SearchProvider>
  );
};

export default App;
