import multiprocessing
import time
from abc import ABC, abstractmethod
class BaseAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    @abstractmethod
    def process_data(self, data):
        pass


    def worker(self,  data_chunk, results, index):
        result = [self.process_data(data) for data in data_chunk]
        results[index] = result

    def run(self,num_workers):        
        # Example data to process
        data_list = [f"data_{i}" for i in range(20)]
        num_workers = num_workers  # Number of processes to use
        
        # Split data_list into chunks for each worker
        data_chunks = [data_list[i::num_workers] for i in range(num_workers)]
        
        # Create a manager to store results from different processes
        manager = multiprocessing.Manager()
        results = manager.dict()
        
        processes = []
        
        for i, chunk in enumerate(data_chunks):
            process = multiprocessing.Process(target=self.worker, args=(chunk, results, i))
            processes.append(process)
            process.start()
        
        for process in processes:
            process.join()
        
        final_results = []
        for i in range(num_workers):
            final_results.extend(results[i])
            # print(final_results)
        return final_results


