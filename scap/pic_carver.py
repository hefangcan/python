import re
import zlib
import cv2

from scapy.all import *
pictures_directory = "/home/python/pic_pictures"
face_dierectory ="/home/python/faces"
pcap_file = "man.pcap"


#----------------------------------------------------------------------
def  get_http_headers(http_payload):
    try:
        #print http_payload;
        headers_raw = http_payload[:http_payload.index("GET")]
        print headers_raw
        headers = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n"),headers_raw)
        print headers['Content-Type']
    except:
        return None
    if "Content-Type" not in headers:
        return None
    
    return headers
    
#----------------------------------------------------------------------
def  extract_image(headers,http_payload):
    image = None
    image_type = None
    
    try:
        if "image" in headers['Content-Type']:
            image_type = headers['Content-Type'].split("/")[1]
            
            image = http_payload[http_payload.index("\r\n\r\n")+4:]
            try:
                if "Content-Encoding" in headers.keys():
                    image = zlib.decompress(image,16+zlib.MAX_WBITS)
                elif headers['Content-Encoding'] == "deflate":
                    image = zlib.decompress(image)
            except:
                pass
    except:
        return None,None

    return image,image_type

    

#----------------------------------------------------------------------
def  http_assembler(pcap_file):
    
    carved_images =0
    faces_detected =0
    
    a = rdpcap(pcap_file)
    
    sessions = a.sessions()
    
    for session in sessions:
        
        http_payload = ""
        for packet in sessions[session]:
            try:
                if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                    http_payload += str(packet[TCP].payload)
                    headers_raw = http_payload[:http_payload.index("GET")]
                    print headers_raw;
            except:
                pass
        #print http_payload
        #headers = get_http_headers(http_payload)
        
        if headers is not None:
            for header in headers:
                print header.name
        
        if headers is None:
            continue
        
        
        image,image_type = extract_image(headers,http_payload)
    
        if image is not None and image_type is not None:
            file_name =  "%s-pic_carver_d%.s%" % (pcap_file,carved_images,image_type)
        
            fd = open("%s/%s" % (pictures_directory,file_name),"wb")
        
            fd.write(image)
            fd.close()
        
        
            carved_images +=1
        
            try:
                result = faces_detected("%s/%s" % (pictures_directory,file_name),file_name)
            
                if result is True:
                    faces_detected += 1
            except:
                pass
        
    return carved_images,faces_detected


carved_images,faces_detected = http_assembler(pcap_file)

print "Extracted: %d image" % carved_images
print "Detected: %d faces" % faces_detected
