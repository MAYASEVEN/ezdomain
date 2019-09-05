"""
SOFTWARE: ezdomain 
VERSION : 1.0
AUTHOR  : MAYASEVEN.com
GITHUB  : https://github.com/MAYASEVEN/ezdomain
"""
import urllib2, sys, argparse, time, tqdm
from itertools import chain, product
from termcolor import colored
from multiprocessing import Pool

start = time.time()

def bruteforce(charset, maxlength):
    return (''.join(candidate)
        for candidate in chain.from_iterable(product(charset, repeat=i)
        for i in xrange(1, maxlength + 1)))

def main():
    print """ 
       ____  ___  __    __   _  _     _     ___   _   _
      |        / |  \  |  | | \/ |   / \     |   | \  |
      |>>>>   /  |   | |  | |    |  /___\    |   |  \ |
      |____  /__ |__/  |__| |    | /     \  _|_  |   \|

                                       by MAYASEVEN.com

    """
    parser = argparse.ArgumentParser(description="""EZdomain is red team tool based on python programming that use to enumerate and scan the domains such as sub-domains, directory, S3 bucket by customizing the position (specific an * in the URL) of the payload and brute-forcing with provided wordlists or string generated.""")
    parser.add_argument("-d", "--domain", type=str, help="Providing a domain name (ex. domain-*.com)")
    parser.add_argument("-w", "--wordlist", type=str, help="Providing a path of a wordlist file")
    parser.add_argument("-b", "--bruteforce", type=str, help="Providing the character set (default are eariotnslcudpmhgbfywkvxzjq0123456789-)")
    parser.add_argument("-m", "--max-length", type=str, help="Providing the max length of string (default is 3)")
    parser.add_argument("-o", "--output", type=str, help="Providing a path of output file")
    parser.add_argument("-t", "--thread", type=str, help="Providing a thread number (default is 3)")
    parser.add_argument("-x", "--exclude", type=str, help="Providing a exclude output status code (ex. -x 443,404)")
    args=parser.parse_args()
    domain=args.domain if args.domain!=None else sys.exit("Please specify the domain, using -d (ex. -d domain-*.com)")
    words=args.wordlist
    global outputfile
    outputfile=args.output
    global exclude
    exclude=args.exclude.split(",") if args.exclude!=None else "999"
    thread=args.thread or 3
    bruteforce_text=args.bruteforce or "eariotnslcudpmhgbfywkvxzjq0123456789-"
    max_length=args.max_length or 3 
    try:
        if(words!=None):
            file = open(words, 'r')
            word = file.readlines()
	else:
	    word = list(bruteforce(bruteforce_text, int(max_length)))
        p = Pool(processes=int(thread))
        pbar = tqdm.tqdm(p.imap_unordered(checkurl, [domain.replace('*', x.split('\n')[0]) for x in word]),
	    total=len(word), desc="[Progress]", unit="word")
	for message in pbar:
	    if(message!=None):
	        pbar.write("\r"+" "*100+"\r"+message) 
	        pbar.update()
	        time.sleep(0.1)
    except KeyboardInterrupt:
	p.terminate()
	sys.exit()
    except Exception as e:
        print "Error messages: {%s} \nusage: python ezdomain.py -h" % e
	sys.exit()

def checkurl(url):
    if(outputfile!=None):
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
    if(outputfile!=None):
        sys.stdout = output 
        sys.stdout.flush()
    return status

if __name__ == "__main__":
    main()

