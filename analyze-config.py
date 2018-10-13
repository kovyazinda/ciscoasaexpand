import sys
import re
import csv

inputfile = sys.argv[1]
outputfile = sys.argv[2]

if inputfile and outputfile:

  print "Reading:"+inputfile

  infile=open(inputfile,"rU")
  outfile=open(outputfile,"w+")

  csvrecord = csv.writer(outfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)

  prevgroup = ""
  preprevgroup = ""
  currentgroup = ""
  netobjectvalue = ""
  currentitem=[]
  netgrouplist=[]
  aclstring=[]

  objectdict = {}

  for string in infile:
   

   match = re.search("^object-group.*", string)
   if match:
    for netobject in currentitem:
     netobjectvalue=netobjectvalue+netobject+","


    checkproto = re.search("^.*\ (tcp|udp)",currentgroup)
    if checkproto:
     serviceobject=re.sub("\ (tcp|udp)",'',checkproto.group(0))

     objectdict[serviceobject]=checkproto.group(0)+netobjectvalue 
    else: 
     objectdict[currentgroup]=netobjectvalue
  
    preprevgroup=prevgroup
    prevgroup=currentgroup
    currentgroup=re.sub("object-group\ (network|service)*\ ",'',match.group(0))

    currentitem=[]
    netobjectvalue=""

   child = re.search("^\ .*object.*", string)
   if child:
    currentitem.append(re.sub(".*object\ (object|host|service|fqdn|eq)",'',child.group(0)))

   acl = re.search("^access-list",string)
   remark = re.search("remark",string)
   if acl and not remark:
    aclstring=string.split(" ")
    aclentryincrement=0
    for aclentry in aclstring:
     aclentryincrement+=1
     for dictentry in objectdict: 
      if aclentry == dictentry:
       print ""
       aclstring[aclentryincrement-1]=(aclentry+"("+objectdict[dictentry]+")")      
    csvrecord.writerow(aclstring)

    
 
#print collected datastructure from objects
#  print objectdict
  
  rulerow=[]
  rulerow.append("")
  csvrecord.writerow(rulerow)

  for word in objectdict:
   rulerow.append(word)
   rulerow.append(objectdict[word])
   csvrecord.writerow(rulerow)
   rulerow=[]

  outfile.close
  infile.close

