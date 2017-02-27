import sys, HTSeq, subprocess
try:
	forward = sys.argv[1]
	reverse = sys.argv[2]
	output = sys.argv[3]
except:
	print "Usage: python kalishrb_16s_pipeline.py <forward fastq> <reverse fastq> <output file prefix (example.q20)>"
	sys.exit()

mefit = 'mefit'+' -s '+output+' -r1 '+ forward+ ' -r2 '+ reverse+ ' -nonovlp '+ '-n 15 '+ '-avgq 20'
subprocess.check_call(mefit, shell=True)

ovlp = "".join([output, ".ovlp.hq.fastq "])
nonovlp = "".join([output, ".nonovlp.hq.fastq"])
combined = "".join([output, ".combined.hq.fastq"])
cat = "".join(['cat ', ovlp, nonovlp, ' > ', combined])

subprocess.Popen(cat , shell=True).wait()

f1name= combined
f1namefasta=f1name[:-6]+".fasta"

f1=open(f1name,'r')
f2=open(f1namefasta,'w')
count = 0
for r in HTSeq.FastqReader(f1):
        count += 1
        r.write_to_fasta_file(f2)
f1.close()
f2.close()


nochimera = "".join([output, ".hq.nochimera.fasta"])
uchime = "".join(['usearch ', '-uchime2_ref ', combined, ' -db ', '/usr/local/bnfo/refdb/SILVA123/rep_set/rep_set_16S_only/97/97_otus_16S.udb ', '-notmatched ', nochimera, ' -strand plus -mode balanced -threads 8'])
subprocess.check_call(uchime, shell=True)
rdp = "".join(['java ', '-Xmx2g -jar /usr/local/bnfo/rdp_classifier_2.12/dist/classifier.jar classify -f filterbyconf -c 0.80 -o rdp_output.txt -h rdp_hier.txt ', nochimera])
subprocess.check_call(rdp, shell=True)
usearch = "".join(['sh /usr/local/bnfo/scripts/usearch_otu_pipeline.sh ', '-s ', output, ' -f ', f1namefasta, ' -r 3.0 -i 0.90 -d /usr/local/bnfo/refdb/SILVA123/forUsearch/97_otus_16S.forUsearch.udb'])
subprocess.check_call(usearch, shell=True)