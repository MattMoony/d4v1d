import { Flex, Switch, Text } from '@theme-ui/components';
import * as React from 'react';
import { Box, Label } from 'theme-ui';

type SettingProps = {
  label: string;
  toggled: boolean;
  onToggle: ()=>void;
};

const Setting = ({ label, toggled, onToggle, }: SettingProps) => {
  return (
    <Flex sx={{
      justifyContent: 'space-between',
      alignItems: 'center',
    }}>
      <Label sx={{
        flex: 1,
      }}>
        {label}
      </Label>
      <Box>
        <Switch checked={toggled} onClick={onToggle} />
      </Box>
    </Flex>
  );
};

export default Setting;