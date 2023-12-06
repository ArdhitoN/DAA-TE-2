# Partition the values with those before index start_index fixed.
# test_assignment is the test assignment so far.
# test_value = total value of the first set in test_assignment.
# Initially best assignment and its error are in
# best_assignment and best_err.
def find_partition_branch_and_bound(values, start_index, total_value, unassigned_value, test_assignment, test_value, best_assignment, best_err):
    # If start_index is beyond the end of the array,
    # then all entries have been assigned.
    if start_index >= len(values):
        # We're done. See if this assignment is better than
        # what we have so far.
        test_err = abs(2 * test_value - total_value)
                

        if test_err == 0:
            best_err[0] = test_err
            best_assignment[:] = test_assignment[:]
            
            return 0
        
        if test_err < best_err[0]:
            # This is an improvement. Save it.
            best_err[0] = test_err
            best_assignment[:] = test_assignment[:]

            return best_err[0]

        return best_err[0]


    else:
        # See if there's any way we can assign
        # the remaining items to improve the solution.
        test_err = abs(2 * test_value - total_value)
        if test_err - unassigned_value < best_err[0]:
            # There's a chance we can make an improvement.
            # We will now assign the next item.
            unassigned_value -= values[start_index]

            # Try adding values[start_index] to set 1.
            test_assignment[start_index] = True
            best_error = find_partition_branch_and_bound(values, start_index + 1,
                                         total_value, unassigned_value,
                                         test_assignment, test_value + values[start_index],
                                         best_assignment, best_err)
            if best_error == 0:
                return 0
            
            # Try adding values[start_index] to set 2.
            test_assignment[start_index] = False
            return find_partition_branch_and_bound(values, start_index + 1,
                                         total_value, unassigned_value,
                                         test_assignment, test_value,
                                         best_assignment, best_err)
            
         
def bnb_final(values):
    total_value = sum(values)
    if total_value % 2 != 0:
        print(False)
        return False  
    
    best_err = [float('inf')]
    best_assignment = [False] * len(values)
    rslt = find_partition_branch_and_bound(values, 0, total_value, total_value, best_assignment, 0, best_assignment, best_err)
    print(rslt == 0)
    return rslt == 0
