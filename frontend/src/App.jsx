import React from 'react';
import { Box, Flex } from '@chakra-ui/react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import PackageTable from './components/PackageTable';

function App() {
  return (
    <Flex direction="column" height="100vh">
      <Navbar />
      <Flex flex="1">
        <Sidebar />
        <Box flex="1" overflowY="auto" p={4}>
          <PackageTable />
        </Box>
      </Flex>
    </Flex>
  );
}

export default App;

