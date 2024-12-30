import { useState } from "react";
import { Button as ChakraButton, HStack } from "@chakra-ui/react";
import { Play, Grid } from "lucide-react";

const Button = () => {
  const [isLiveSelected, setIsLiveSelected] = useState(false); 
  const [isHighlightsSelected, setIsHighlightsSelected] = useState(false); 

  const handleLiveClick = () => {
    setIsLiveSelected(!isLiveSelected); 
  };

  const handleHighlightsClick = () => {
    setIsHighlightsSelected(!isHighlightsSelected);
  };

  return (
    <HStack p={4}>
      {/* Live button */}
      <ChakraButton
        bg={isLiveSelected ? "#0273C3" : "gray.200"}
        color={isLiveSelected ? "white" : "gray.600"} 
        _hover={{ bg: isLiveSelected ? "#025a93" : "gray.200" }} 
        px={6}
        variant="ghost"
        onClick={handleLiveClick} 
      >
        <Play size={16} style={{ marginRight: "8px" }} />
        Live
      </ChakraButton>

      {/* Highlights button */}
      <ChakraButton
        bg={isHighlightsSelected ? "#0273C3" : "gray.200"} 
        color={isHighlightsSelected ? "white" : "gray.600"} 
        _hover={{ bg: isHighlightsSelected ? "#025a93" : "gray.200" }} 
        px={6}
        variant="ghost"
        onClick={handleHighlightsClick} 
      >
        <Grid size={16} style={{ marginRight: "8px" }} />
        Highlights
      </ChakraButton>
    </HStack>
  );
};

export default Button;
