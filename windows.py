# just playing around with wmi
import wmi

w = wmi.WMI()

os = w.Win32_OperatingSystem()
if len(os) == 1:
	os = os[0]

perf = w.Win32_PerfFormattedData_PerfOS_System()
if len(perf) == 1:
	perf = perf[0]
	
if __name__ == "__main__":
	print "OS data"
	print os
	print "Performance data"
	print perf
else:
	print "Windows.py loaded"
	print "windows.os object == Win32_OperatingSystem()"
	print "windows.perf object == Win32_PerfFormattedData_PerfOS_System()"