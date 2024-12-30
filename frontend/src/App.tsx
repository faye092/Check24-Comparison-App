import React from "react";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import NavControls from "./components/NavControls";
import { Box } from "@chakra-ui/react";

const App: React.FC = () => {

  return (
    <Box minH="100vh" bg="gray.50" p={0}>
      <Navbar
        onSearch={(query: string) => console.log("Search query:", query)}
      />
      <NavControls />
      <Box display="flex" flex="1" bg="gray.50">
         <Sidebar />
        <Box flex="1" p="6" textAlign="center">
          <p>Main Content Area</p>
        </Box>
      </Box>
    </Box>
  );
};

export default App;
