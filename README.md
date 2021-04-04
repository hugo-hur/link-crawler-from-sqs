# link-crawler-from-sqs
Reads url:s from sqs, opens them, crawls those pages for links to threads and pushes those links to sqs for other crawler workers to find and process elsewhere.
