import { useState } from 'react'
import {
  HStack,
  Text,
  Input,
  Button,
} from "@chakra-ui/react"

const TimePeriod = () => {
  const [startDate, setStartDate] = useState("")
  const [endDate, setEndDate] = useState("")

  const canApply = startDate && endDate

  return (
    <HStack p={4} align="center">
      <Text fontWeight="medium">Select Date Range:</Text>
      <HStack p={2}>
        <Input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          size="sm"
          width="150px"
          placeholder="Start Date"
        />
        <Text>-</Text>
        <Input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          size="sm"
          width="150px"
          placeholder="End Date"
        />
      </HStack>
      <HStack p={2}>
        <Button
          size="sm"
          variant="ghost"
          onClick={() => {
            setStartDate("")
            setEndDate("")
          }}
        >
          Reset
        </Button>
        <Button
          size="sm"
          bg={canApply ? "#0273C3" : "gray.400"}
          color="white"
          _hover={{ bg: canApply ? "#0264A8" : "gray.600" }}
          disabled={!canApply}
        >
          Apply
        </Button>
      </HStack>
    </HStack>
  )
}

export default TimePeriod