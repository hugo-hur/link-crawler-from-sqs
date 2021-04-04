import boto3
from multiprocessing import Pool
from crawl_board_sqs import crawl_board_to_sqs

#Set sub boards to crawl
boards = ["anime", "ohjelmointi", "sekalainen", "tori", "masiinat"]
boards_whole=[]
for board in boards:
    boards_whole.append("https://ylilauta.org/" + board)

    
def parallel_link_crawl(num_threads, boards_list):
    
    out = []
    with Pool(num_threads) as p:
        sublists = p.map(crawl_board_to_sqs, boards_list)
        p.close()
        p.join()
        return sum(sublists)
    
    
numThreads = parallel_link_crawl(num_threads=4, boards_list=boards_whole)
print(numThreads)
