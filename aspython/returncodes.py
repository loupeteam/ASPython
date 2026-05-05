"""B&R Automation Studio build / PVI Transfer return codes."""

ASReturnCodes = {
    "Errors-Warnings": 3,
    "Errors": 2,
    "Warnings": 1,
    "None": 0,
}

PVIReturnCodeText = {
    0: 'Application completed successfully',
    28320: 'File not found (.PIL file or "call" command)',
    28321: 'Filename not specified (command line parameter)',
    28322: 'Unable to load BRErrorLB.DLL ("ReadErrorLogBook" command)',
    28323: 'DLL entry point not found ("ReadErrorLogBook" command)',
    28324: 'BR module not found ("Download" command)',
    28325: 'Syntax error in command line',
    28326: 'Unable to start PVI Manager ("StartPVIMan" command)',
    28327: 'Unknown command',
    28328: 'Unable to connect ("Connection" command with "C" parameter)',
    28329: 'Unable to establish connection in bootstrap loader mode',
    28330: 'Error transferring operating system in bootstrap loader mode',
    28331: 'Process aborted',
    28332: 'The specified directory doesn\'t exist',
    28333: 'No directory specified',
    28334: 'The application used to create an AR update file wasn\'t found ("ARUpdateFileGenerate" command)',
    28335: 'The specified AR base file (*.s*) is invalid ("ARUpdateFileGenerate" command)',
    28336: 'Error creating the AR update file ("ARUpdateFileGenerate" command)',
    28337: 'There is no valid connection to the PLC. In order to be able to read the CAN baud rate, the CAN ID or the CAN node number, you need a connection to the PLC',
    28338: 'The specified logger module doesn\'t exist on PLC ("Logger" command)',
    28339: 'The specified .br file is not a valid logger module ("Logger" command)',
    28340: 'The .pil file does not contain any information about the AR version to be installed.',
    28341: 'Transfer to the corresponding target system is not possible since the AR version on the target system does not yet support the transfer mode',
}
