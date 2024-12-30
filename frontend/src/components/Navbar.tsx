import React, { useState } from "react";
import { Box, Flex, Input, IconButton, HStack, Image } from "@chakra-ui/react";
import { Search } from "lucide-react";

interface NavbarProps {
  onSearch: (query: string) => void;
}

const Navbar: React.FC<NavbarProps> = ({ onSearch }) => {
  const [searchQuery, setSearchQuery] = useState("");
  const [hoveredIcon, setHoveredIcon] = useState<string | null>(null);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
  };

  const handleSearchSubmit = () => {
    onSearch(searchQuery);
  };

  

  const SearchIcon = () => (
    <Box
      onMouseEnter={() => setHoveredIcon('search')}
      onMouseLeave={() => setHoveredIcon(null)}
    >
      <Search 
        size={20} 
        color={hoveredIcon === 'search' ? '#4A5568' : '#718096'} 
      />
    </Box>
  );

  return (
    <Box as="nav" p={4} borderBottom="1px solid #e2e8f0" mb={0}>
      <Flex align="center" justify="space-between">
        {/* Left: Menu button and title */}
        <HStack gap={4}>
          <Image
            src="/check24-nav.png" 
            alt="Check24 Logo"
            height="25px"
            objectFit="contain"
          />
          <Box fontWeight="bold" color="gray.700" fontSize="xl">Football Streaming Comparison</Box>
        </HStack>

        {/* Right: Search box and filter buttons */}
        <HStack gap={4} align="center">
          <Box position="relative" width="700px">
            <Input
              placeholder="Search tournaments or teams..."
              value={searchQuery}
              onChange={handleSearchChange}
              paddingRight="40px"
              height="40px" 
            />
            <Box
              position="absolute"
              right="8px"
              top="50%"
              transform="translateY(-50%)"
              display="flex"
              alignItems="center"
              justifyContent="center"
              height="100%"
            >
              <IconButton
                aria-label="Search"
                as={SearchIcon}
                variant="ghost"
                bg="transparent"
                onClick={handleSearchSubmit}
                height="auto"
                minWidth="auto"
                padding={0}
              />
            </Box>
          </Box>
        </HStack>
      </Flex>
    </Box>
  );
};

export default Navbar;