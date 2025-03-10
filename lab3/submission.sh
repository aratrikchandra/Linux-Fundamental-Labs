# Extract columns
cut -f1,2 employees1.txt > part1.txt
cut -f3 employees2.txt > part2.txt
cut -f2,3 employees3.txt > part3.txt

# Combine columns
paste part1.txt part2.txt part3.txt > combined.txt

# Filter HR department
# Remove duplicates by sorting EmployeeID and using uniq
awk -F'\t' '$5 == "HR"' combined.txt | sort -k1n | uniq -w 3 > deduped.txt

# Sort by Salary descending
sort -nrk4 deduped.txt > output.txt