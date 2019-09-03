import urllib2, sys, argparse, time, tqdm
from termcolor import colored
from multiprocessing import Pool

start = time.time()

def main():
    parser = argparse.ArgumentParser(description="""ezdomain is a useful red-team tool to enumerate the target domain such as sub-domain, directory scanning, s3 bucket, etc.""")
    parser.add_argument("-d", "--domain", type=str, help="Providing a domain name (ex. domain-*.com)")
    parser.add_argument("-w", "--wordlist", type=str, help="Providing a path of a wordlist file")
    parser.add_argument("-o", "--output", type=str, help="Providing a path of output file")
    parser.add_argument("-t", "--thread", type=str, help="Providing a thread number (default is 3)")
    parser.add_argument("-x", "--exclude", type=str, help="Providing a exclude output status code (ex. -x 443,404)")
    args=parser.parse_args()
    domain=args.domain
    words=args.wordlist
    global outputfile
    outputfile=args.output
    global exclude
    exclude=args.exclude.split(",") if args.exclude!=None else "999"
    thread=args.thread or 3
    try:
        file = open(words, 'r')
        word = file.readlines()
	p = Pool(processes=int(thread))
	pbar = tqdm.tqdm(p.imap_unordered(checkurl, [domain.replace('*', x.split('\n')[0]) for x in word]),
	            total=len(word), desc="[Progress]", bar_format="{l_bar}{bar} [ Time Left: {remaining} ]")
	for message in pbar:
	    if(message!=None):
	        pbar.write("\r"+" "*100+"\r"+message) 
	        pbar.update()
	        time.sleep(0.1)
    except KeyboardInterrupt:
	p.terminate()
	sys.exit()
    except:
        print "usage: python ezdomain.py -h" 
	sys.exit()

def checkurl(url):
    output = sys.stdout
    sys.stdout = open(outputfile, 'w')
    status = ''
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1'}
        r = urllib2.Request(url, headers=headers)
        conn = urllib2.urlopen(url)
    except urllib2.HTTPError as e:
	if(str(e.code) not in exclude):
	    status = colored('[%s] ', 'red')  % e.code +url
	else: return
    except:
	return 
    else:
        status = colored('[200] ', 'green')+url 
    print status
    return status
    sys.stdout = output 

if __name__ == "__main__":
    main()

