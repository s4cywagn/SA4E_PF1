import asyncio
import aiohttp
import time
import random
import math
import xlsxwriter

BASE_URL = "http://localhost:3000"

async def create_wish(session):
    """
    Asynchronous function to send a POST request using aiohttp session.
    """
    url = f"{BASE_URL}/wishes"
    data = {"text": f"Ich wünsche mir ein Geschenk Nr. {random.randint(1,9999)}"}
    async with session.post(url, json=data) as response:
        return response.status

async def test_load(num_requests):
    """
    Runs num_requests asynchronous tasks in parallel to create wishes.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [create_wish(session) for _ in range(num_requests)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

async def main():
    max_requests = 1.5e6
    exponent = 1.1
    number = 100
    
    results_for_excel = []
    
    while True:
        num_requests = math.ceil(number ** exponent)
        number = num_requests
        if num_requests > max_requests:
            break
        
        print(f"\nStarting load test with {num_requests} requests...")
        start_time = time.time()
        
        results = await test_load(num_requests)
        
        duration = time.time() - start_time
        rps = len(results) / duration if duration else 0
        status_codes = set(results)
        
        print(f"Done! {len(results)} requests in {duration:.2f} seconds.")
        print(f"Requests/sec: {rps:.2f}")
        print(f"Status codes: {status_codes}")
        
        results_for_excel.append([num_requests, duration, rps])
    
    # Write results to Excel
    workbook_name = "load_test_results_async.xlsx"
    workbook = xlsxwriter.Workbook(workbook_name)
    worksheet = workbook.add_worksheet("Results")
    
    worksheet.write(0, 0, "Number of Requests")
    worksheet.write(0, 1, "Duration (seconds)")
    worksheet.write(0, 2, "Requests/Second")

    for i, row_data in enumerate(results_for_excel, start=1):
        worksheet.write(i, 0, row_data[0])
        worksheet.write(i, 1, row_data[1])
        worksheet.write(i, 2, row_data[2])

    workbook.close()
    print(f"\nAll results have been saved to '{workbook_name}'.")

# If you run this script directly:
if __name__ == "__main__":
    asyncio.run(main())
