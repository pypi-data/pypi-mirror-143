# GetTransTool Package

There are four types of methods to extract **longest transcript** or **longest CDS regeion with longest transcript** from **transcripts fasta** file or **GTF** file.

---

- 1.Extract longest transcript from gencode transcripts fasta file.

- 2.Extract longest transcript from gtf format annotation file based on gencode/ensembl/ucsc database.

- 3.Extract longest CDS regeion with longest transcript from gencode database transcripts fasta file.

- 4.Extract longest CDS regeion with longest transcript from gtf format annotation file based on ensembl/ucsc database.

## Install

```shell
$ pip install GetTransTool
```

## Usage

## 1. get longest transcript from gencode transcripts fasta file:

### help infomation:

```shell
$ GetLongestTransFromGencode -h
usage: GetLongestTransFromGencode --file gencode.vM28.transcripts.fa.gz --outfile longest_trans.fa

Get longest transcripts from gencode transcripts fasta file.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -f transfile, --file transfile
                        input your transcripts file with ".gz" format. (gencode.vM28.transcripts.fa.gz)
  -o longestfile, --outfile longestfile
                        output your longest transcript file. (longest_trans.fa)

Thank your for your support, if you have any questions or suggestions please contact me: 3219030654@stu.cpu.edu.cn.
```

### usage:

```shell
$ GetLongestTransFromGencode --file gencode.vM28.transcripts.fa.gz --outfile longest_trans_gencode.fa
Your job is running, please wait...
Your job is done!
Running with 32.33 seconds!
```

there will be three files produced including **name_changed.fa**, **longest_transcripts_info.csv**, **longest_trans_gencode.fa**.

> name_changed.fa:

```
>4933401J01Rik|ENSMUSG00000102693.2|ENSMUST00000193812.2|1070
AAGGAAAGAGGATAACACTTGAAATGTAAATAAAGAAAATACCTAATAAAAATAAATAAA
AACATGCTTTCAAAGGAAATAAAAAGTTGGATTCAAAAATTTAACTTTTGCTCATTTGGT
ATAATCAAGGAAAAGACCTTTGCATATAAAATATATTTTGAATAAAATTCAGTGGAAGAA
...
```

> longest_transcripts_info.csv:

this is the longest transcripts exon length information.

```
fullname,gene_name,translength
snoZ196_ENSMUSG00002074855.1|ENSMUST00020182568.1|35,snoZ196,35
snoZ159_ENSMUSG00002075734.1|ENSMUST00020182611.1|87,snoZ159,87
n-R5s93_ENSMUSG00000119639.1|ENSMUST00000240071.1|119,n-R5s93,119
...
```

> longest_trans_gencode.fa:

this is the filtered longest transcript fasta file.

```
>4933401J01Rik|ENSMUSG00000102693.2|ENSMUST00000193812.2|1070
AAGGAAAGAGGATAACACTTGAAATGTAAATAAAGAAAATACCTAATAAAAATAAATAAA
AACATGCTTTCAAAGGAAATAAAAAGTTGGATTCAAAAATTTAACTTTTGCTCATTTGGT
ATAATCAAGGAAAAGACCTTTGCATATAAAATATATTTTGAATAAAATTCAGTGGAAGAA
...
```

---

## 2. Extract longest transcript from gtf format annotation file based on gencode/ensembl/ucsc database:

### help infomation:

```shell
$ GetLongestTransFromGTF -h
usage: GetLongestTransFromGTF --database ensembl --gtffile Homo_sapiens.GRCh38.101.gtf.gz --genome Homo_sapiens.GRCh38.dna.primary_assembly.fa --outfile longest_trans.fa

Extract longest transcript from gtf format annotation file based on gencode/ensembl/ucsc database.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -d databse, --database databse
                        which annotation database you choose. (default="ensembl", ucsc/ensembl/gencode)
  -g gtffile, --gtffile gtffile
                        input your GTF file with ".gz" format.
  -fa genome, --genome genome
                        your genome fasta file matched with your GTF file with ".gz" format. (Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz)
  -o longestfile, --outfile longestfile
                        output your longest transcript file. (longest_trans.fa)

Thank your for your support, if you have any questions or suggestions please contact me: 3219030654@stu.cpu.edu.cn.
```

### usage:

```shell
$ GetLongestTransFromGTF --database ensembl --gtffile Homo_sapiens.GRCh38.103.gtf.gz --genome Homo_sapiens.GRCh38.dna.primary_assembly.fa --outfile longest_trans_ensembl.fa
Your job is running, please wait...
Your job is done! 
Running with 159.51 seconds!
```

for ucsc:

```
$ GetLongestTransFromGTF --database ucsc --gtffile hg19.ncbiRefSeq.gtf.gz --genome hg19.fa --outfile longest_trans_ucsc.fa
```

---

## 3. Extract longest CDS regeion with longest transcript from gencode database transcripts fasta file.

### help infomation:

```shell
$ GetCDSLongestFromGencode -h
usage: GetCDSLongestFromGencode --file gencode.vM28.pc_transcripts.fa.gz --outfile longest_cds_trans.fa

Extract longest CDS regeion with longest transcript from gencode database transcripts fasta file.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -f transfile, --file transfile
                        input your protein-coding transcripts file with ".gz" format. (gencode.vM28.pc_transcripts.fa.gz)
  -o longestfile, --outfile longestfile
                        output your longest transcript file. (longest_cds_trans.fa)

Thank your for your support, if you have any questions or suggestions please contact me: 3219030654@stu.cpu.edu.cn.
```

### usage:

```shell
$ GetCDSLongestFromGencode --file gencode.vM28.pc_transcripts.fa.gz --outfile longest_cds_trans_gencode.fa
Your job is running, please wait...
Your job is done! 
Running with 17.67 seconds!
```

there will be four files produced including **name_changed.fa**, **All_transcripts_cds_info.csv**, **longest_cds_transcripts_info.csv**, **longest_cds_trans_gencode.fa**.

> name_changed.fa:

```
>Xkr4_ENSMUSG00000051951.6_ENSMUST00000070533.5_151_2094_3634
GCGGCGGCGGGCGAGCGGGCGCTGGAGTAGGAGCTGGGGAGCGGCGCGGCCGGGGAAGGA
AGCCAGGGCGAGGCGAGGAGGTGGCGGGAGGAGGAGACAGCAGGGACAGGTGTCAGATAA
AGGAGTGCTCTCCTCCGCTGCCGAGGCATCATGGCCGCTAAGTCAGACGGGAGGCTGAAG
...
```

> All_transcripts_cds_info.csv:

this is the all transcripts cds and exon length information.

```
fullname,gene_name,translength,cdslength
>mt-Nd6_ENSMUSG00000064368.1_ENSMUST00000082419.1_1_519_519,>mt-Nd6,519,519
>mt-Nd5_ENSMUSG00000064367.1_ENSMUST00000082418.1_1_1824_1824,>mt-Nd5,1824,1824
>mt-Nd4l_ENSMUSG00000065947.1_ENSMUST00000084013.1_1_297_297,>mt-Nd4l,297,297
...
```

> longest_cds_transcripts_info.csv:

```
fullname,gene_name,translength,cdslength
>mt-Nd6_ENSMUSG00000064368.1_ENSMUST00000082419.1_1_519_519,>mt-Nd6,519,519
>mt-Nd5_ENSMUSG00000064367.1_ENSMUST00000082418.1_1_1824_1824,>mt-Nd5,1824,1824
>mt-Nd4l_ENSMUSG00000065947.1_ENSMUST00000084013.1_1_297_297,>mt-Nd4l,297,297
...
```

> longest_cds_trans_gencode.fa:

```
>Xkr4_ENSMUSG00000051951.6_ENSMUST00000070533.5_151_2094_3634
GCGGCGGCGGGCGAGCGGGCGCTGGAGTAGGAGCTGGGGAGCGGCGCGGCCGGGGAAGGA
AGCCAGGGCGAGGCGAGGAGGTGGCGGGAGGAGGAGACAGCAGGGACAGGTGTCAGATAA
AGGAGTGCTCTCCTCCGCTGCCGAGGCATCATGGCCGCTAAGTCAGACGGGAGGCTGAAG
...
```

---

## 4. Extract longest CDS regeion with longest transcript from gtf format annotation file based on ensembl/ucsc database.

### help infomation:

```shell
$ GetCDSLongestFromGTF -h
usage: GetCDSLongestFromGTF --database ensembl --gtffile Homo_sapiens.GRCh38.101.gtf.gz --genome Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz --outfile longest_cds_trans.fa

Extract longest CDS regeion with longest transcript from gtf format annotation file based on ensembl/ucsc database.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -d databse, --database databse
                        which annotation database you choose. (default="ensembl", ucsc/ensembl)
  -g gtffile, --gtffile gtffile
                        input your GTF file with ".gz" format.
  -fa genome, --genome genome
                        your genome fasta file matched with your GTF file with ".gz" format. (Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz)
  -o cdslongestfile, --outfile cdslongestfile
                        output your longest transcript file. (longest_cds_trans.fa)

Thank your for your support, if you have any questions or suggestions please contact me: 3219030654@stu.cpu.edu.cn.
```

### usage:

```shell
$ GetCDSLongestFromGTF  --database ensembl --gtffile Homo_sapiens.GRCh38.103.gtf.gz --genome Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz --outfile longest_cds_trans_ensembl.fa
Your job is running, please wait...
Your job is done! 
Running with 152.38 seconds!
```

for ucsc:

```shell
$ GetCDSLongestFromGTF  --database ucsc --gtffile hg19.ncbiRefSeq.gtf.gz --genome hg19.fa.gz --outfile longest_cds_trans_ensembl.fa
```

---

## END

> Thank your for your support, if you have any questions or suggestions please contact me: 3219030654@stu.cpu.edu.cn.