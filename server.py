import clr #package pythonnet, not clr
import serial


openhardwaremonitor_hwtypes = ['Mainboard','SuperIO','CPU','RAM','GpuNvidia','GpuAti','TBalancer','Heatmaster','HDD']
openhardwaremonitor_sensortypes = ['Voltage','Clock','Temperature','Load','Fan','Flow','Control','Level','Factor','Power','Data','SmallData']



def initialize_openhardwaremonitor():
    file = 'OpenHardwareMonitorLib'
    clr.AddReference(file)

    from OpenHardwareMonitor import Hardware

    handle = Hardware.Computer()
    handle.MainboardEnabled = True
    handle.CPUEnabled = True
    handle.RAMEnabled = True
    handle.GPUEnabled = True
    handle.HDDEnabled = True
    handle.Open()
    return handle

def initialize_cputhermometer():
    file = 'CPUThermometerLib'
    clr.AddReference(file)

    from CPUThermometerLib import Hardware
    handle = Hardware.Computer()
    handle.CPUEnabled = True
    handle.Open()
    return handle

def fetch(handle):
    gpu_temp = 0
    cpu_temp_sum = 0
    cpu_cores = 0
    for i in handle.Hardware:
        i.Update()
        for sensor in i.Sensors:
            if sensor.Value is not None:
                if(sensor.Hardware.HardwareType == 2): # cpu
                    if type(sensor).__module__ == 'OpenHardwareMonitor.Hardware':
                        sensortypes = openhardwaremonitor_sensortypes
                        hardwaretypes = openhardwaremonitor_hwtypes
                    else:
                        return
                    if sensor.SensorType == sensortypes.index('Temperature'):
                        #print(sensor.Hardware.HardwareType)
                        print(u"%s %s Temperature Sensor #%i %s - %s\u00B0C" % (hardwaretypes[sensor.Hardware.HardwareType], sensor.Hardware.Name, sensor.Index, sensor.Name, sensor.Value))
                        cpu_cores += 1
                        cpu_temp_sum += float(sensor.Value)
                if(sensor.Hardware.HardwareType == 4): # gpu
                    if type(sensor).__module__ == 'OpenHardwareMonitor.Hardware':
                        sensortypes = openhardwaremonitor_sensortypes
                        hardwaretypes = openhardwaremonitor_hwtypes
                    else:
                        return
                    if sensor.SensorType == sensortypes.index('Temperature'):
                        #print(sensor.Hardware.HardwareType)
                        print(u"%s %s Temperature Sensor #%i %s - %s\u00B0C" % (hardwaretypes[sensor.Hardware.HardwareType], sensor.Hardware.Name, sensor.Index, sensor.Name, sensor.Value))
                        gpu_temp += float(sensor.Value)
    if(cpu_cores == 0):
        print('No cpu temperature sensors were found.')
        cpu_temp = 0
    else:
        cpu_temp = cpu_temp_sum / cpu_cores

    
    return round(cpu_temp, 1), round(gpu_temp, 1)
    


def fetch_stats(handle):
    for i in handle.Hardware:
        i.Update()
        for sensor in i.Sensors:
            parse_sensor(sensor)
        for j in i.SubHardware:
            j.Update()
            for subsensor in j.Sensors:
                parse_sensor(subsensor)

def parse_sensor(sensor):
        if sensor.Value is not None:
            if type(sensor).__module__ == 'OpenHardwareMonitor.Hardware':
                sensortypes = openhardwaremonitor_sensortypes
                hardwaretypes = openhardwaremonitor_hwtypes
            else:
                return

            if sensor.SensorType == sensortypes.index('Temperature'):
                print(sensor.Hardware.HardwareType)
                print(u"%s %s Temperature Sensor #%i %s - %s\u00B0C" % (hardwaretypes[sensor.Hardware.HardwareType], sensor.Hardware.Name, sensor.Index, sensor.Name, sensor.Value))

def open_port(portname):
    return serial.Serial(portname, 9600, timeout=0)

if __name__ == "__main__":
    serial = open_port('COM3')
    while(True):
        print("OpenHardwareMonitor:")
        HardwareHandle = initialize_openhardwaremonitor()
        cpu_temp, gpu_temp = fetch(HardwareHandle)

        serial.write(b'c')
        serial.write(str(cpu_temp).encode())
        serial.write(b's')


        serial.write(b'g')
        serial.write(str(gpu_temp).encode())
        serial.write(b's')


        #fetch_stats(HardwareHandle)
        #print("\nCPUMonitor:")
        #CPUHandle = initialize_cputhermometer()
        #fetch_stats(CPUHandle)
        #print()