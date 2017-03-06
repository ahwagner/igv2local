# igv2local
a command-line interface for moving IGV sessions from remote host to local

## Installation
`igv2local` requires Python version >= 3.6
`pip install git+https://github.com/ahwagner/igv2local --process-dependency-links`

## Configuration
`igv2local` only requires the remote host configuration specified by the `gmstk` dependency. If this was not previously set up, `igv2local` will prompt you for the host details. The username and host may be saved to the gmstk `config.py` file for future use by responding 'y' to the save prompt.

```bash
igv2local -h
Remote host credentials unspecified.
Please enter the remote hostname: <your host machine name, e.g. linus199>
Please enter the remote username: <your username on the host machine, e.g. jsmith>
Save to configuration file? (y/N): y
```

If your machine is not authorized via SSH keys, you will be prompted for your remote host password each time you use `igv2local`.

```bash
igv2local -h
Remote host credentials unspecified.
Please enter the remote hostname: <your host machine name, e.g. linus199>
Please enter the remote username: <your username on the host machine, e.g. jsmith>
Save to configuration file? (y/N): y
Authentication failed. Please specify password for jsmith on linus199.
Password: 
```
## Example
```bash
igv2local https://gscweb.gsc.wustl.edu/gscmnt/gc2547/griffithlab/awagner/web_test.xml
```
