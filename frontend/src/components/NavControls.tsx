import { Box, HStack, VStack } from "@chakra-ui/react";
import Button from './Button';
import TimePeriod from './TimePeriod';

const NavControls = () => {
  return (
    <Box 
      px={2} 
      py={2} 
      borderBottom="1px solid" 
      borderColor="gray.200" 
      bg="white"
    >
      <HStack p={2} align="center">
        {/* Buttons for Live and Highlights */}
        <Button />

        {/* Custom Divider */}
        <Box 
          width="1px" 
          height="32px" 
          bg="gray.300" 
        />

        {/* Time Period Selector */}
        <VStack align="start" p={0}>
          <TimePeriod />
        </VStack>
      </HStack>
    </Box>
  );
};

export default NavControls;
