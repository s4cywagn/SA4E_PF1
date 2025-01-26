import pandas as pd

def extend_requests_until_7_billion(input_excel_path: str, output_excel_path: str) -> None:
    """
    Reads an Excel file with columns: 'Requests', 'Duration', 'Requests/Second'.
    Calculates the mean of 'Requests/Second' from known data.
    Extends rows until 'Requests' exceed 7,000,000,000 using:
        next_Requests = (previous_Requests) ^ 1.1
        next_Requests_Second = mean(Requests/Second)
        next_Duration = next_Requests / next_Requests_Second
    Saves the extended DataFrame to a new Excel file.
    """
    # 1. Read the input Excel file
    df = pd.read_excel(input_excel_path)

    # 2. Compute the mean of 'Requests/Second'
    mean_rps = df['Requests/Second'].mean()

    # 3. Start extending from the last row in the DataFrame
    last_requests = df['Requests'].iloc[-1]

    # 4. Loop until requests exceed 7 billion
    new_data = []
    while last_requests <= 7_000_000_000_0:
        # Calculate new requests
        next_requests = last_requests ** 1.1
        
        # If we've gone beyond 7 billion, stop
        if next_requests > 7_000_000_000:
            break
        
        # Calculate new duration = requests / requests_per_second
        next_duration = next_requests / mean_rps
        
        # Store new row in a temporary list
        new_data.append({
            'Requests': next_requests,
            'Duration': next_duration,
            'Requests/Second': mean_rps
        })
        
        # Update 'last_requests' for the next iteration
        last_requests = next_requests

    # 5. Create a DataFrame from new_data
    df_extended = pd.DataFrame(new_data)
    
    # 6. Concatenate original and new data
    df_result = pd.concat([df, df_extended], ignore_index=True)

    # 7. Write the extended DataFrame to a new Excel file
    df_result.to_excel(output_excel_path, index=False)
    print(f"Extended data saved to: {output_excel_path}")


if __name__ == "__main__":
    # Adjust these paths and file names as appropriate
    input_file = "load_test_results_async.xlsx"
    output_file = "extended_output.xlsx"
    
    extend_requests_until_7_billion(input_file, output_file)
