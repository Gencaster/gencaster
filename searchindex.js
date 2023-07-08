Search.setIndex({docnames:["back/api/gencaster","back/api/index","back/api/story_graph","back/api/stream","back/graphql","back/index","back/osc_server","deployment","editor","front","index","quickstart","services","sound","story_graph"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":4,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,"sphinx.ext.intersphinx":1,"sphinx.ext.todo":2,"sphinx.ext.viewcode":1,sphinx:56},filenames:["back/api/gencaster.rst","back/api/index.rst","back/api/story_graph.rst","back/api/stream.rst","back/graphql.rst","back/index.rst","back/osc_server.rst","deployment.rst","editor.rst","front.rst","index.rst","quickstart.rst","services.rst","sound.rst","story_graph.rst"],objects:{"":[[0,0,0,"-","gencaster"],[6,0,0,"-","osc_server"],[2,0,0,"-","story_graph"],[3,0,0,"-","stream"]],"gencaster.distributor":[[0,1,1,"","GenCasterChannel"],[0,1,1,"","GraphQLWSConsumerInjector"],[0,1,1,"","GraphUpdateMessage"],[0,3,1,"","MissingChannelLayer"],[0,1,1,"","NodeUpdateMessage"],[0,4,1,"","uuid_to_group"]],"gencaster.distributor.GenCasterChannel":[[0,2,1,"","__init__"]],"gencaster.distributor.GraphQLWSConsumerInjector":[[0,2,1,"","__init__"],[0,2,1,"","receive"],[0,2,1,"","websocket_disconnect"]],"gencaster.distributor.GraphUpdateMessage":[[0,2,1,"","__init__"]],"gencaster.distributor.NodeUpdateMessage":[[0,2,1,"","__init__"]],"gencaster.schema":[[0,1,1,"","AuthStrawberryDjangoField"],[0,1,1,"","IsAuthenticated"],[0,1,1,"","LoginError"],[0,1,1,"","Mutation"],[0,1,1,"","Query"],[0,1,1,"","Subscription"],[0,1,1,"","User"],[0,4,1,"","graphql_check_authenticated"],[0,4,1,"","update_or_create_audio_cell"]],"gencaster.schema.LoginError":[[0,2,1,"","__init__"]],"gencaster.schema.Mutation":[[0,2,1,"","__init__"],[0,2,1,"","add_edge"],[0,2,1,"","add_node"],[0,2,1,"","create_script_cells"],[0,2,1,"","delete_edge"],[0,2,1,"","delete_node"],[0,2,1,"","delete_script_cell"],[0,2,1,"","update_audio_file"],[0,2,1,"","update_node"]],"gencaster.schema.Query":[[0,2,1,"","__init__"]],"gencaster.schema.Subscription":[[0,2,1,"","__init__"]],"gencaster.schema.User":[[0,2,1,"","__init__"]],"gencaster.settings":[[0,0,0,"-","base"],[0,0,0,"-","deploy_dev"],[0,0,0,"-","dev"],[0,0,0,"-","dev_local"],[0,0,0,"-","test"]],"osc_server.exceptions":[[6,3,1,"","MalformedOscMessage"],[6,3,1,"","OscBackendAuthException"]],"osc_server.server":[[6,1,1,"","OSCServer"]],"osc_server.server.OSCServer":[[6,2,1,"","__init__"],[6,2,1,"","acknowledge_handler"],[6,2,1,"","beacon_handler"],[6,2,1,"","remote_action_handler"]],"story_graph.engine":[[2,1,1,"","Engine"],[2,3,1,"","ScriptCellTimeout"]],"story_graph.engine.Engine":[[2,2,1,"","__init__"],[2,2,1,"","execute_audio_cell"],[2,2,1,"","execute_markdown_code"],[2,2,1,"","execute_node"],[2,2,1,"","execute_sc_code"],[2,2,1,"","get_stream_variables"],[2,2,1,"","start"]],"story_graph.markdown_parser":[[2,1,1,"","GencasterRenderer"],[2,1,1,"","GencasterToken"],[2,4,1,"","md_to_ssml"]],"story_graph.markdown_parser.GencasterRenderer":[[2,2,1,"","__init__"],[2,2,1,"","add_break"],[2,2,1,"","chars"],[2,2,1,"","eval_python"],[2,2,1,"","exec_python"],[2,2,1,"","female"],[2,2,1,"","male"],[2,2,1,"","moderate"],[2,2,1,"","raw_ssml"],[2,2,1,"","validate_gencaster_tokens"],[2,2,1,"","var"]],"story_graph.markdown_parser.GencasterToken":[[2,2,1,"","__init__"]],"story_graph.models":[[2,1,1,"","AudioCell"],[2,1,1,"","CellType"],[2,1,1,"","Edge"],[2,1,1,"","Graph"],[2,1,1,"","Node"],[2,1,1,"","ScriptCell"]],"story_graph.models.AudioCell":[[2,3,1,"","DoesNotExist"],[2,3,1,"","MultipleObjectsReturned"],[2,1,1,"","PlaybackChoices"]],"story_graph.models.Edge":[[2,3,1,"","DoesNotExist"],[2,3,1,"","MultipleObjectsReturned"]],"story_graph.models.Graph":[[2,3,1,"","DoesNotExist"],[2,1,1,"","GraphDetailTemplate"],[2,3,1,"","MultipleObjectsReturned"],[2,1,1,"","StreamAssignmentPolicy"],[2,2,1,"","acreate_entry_node"],[2,2,1,"","aget_entry_node"]],"story_graph.models.Node":[[2,3,1,"","DoesNotExist"],[2,3,1,"","MultipleObjectsReturned"]],"story_graph.models.ScriptCell":[[2,3,1,"","DoesNotExist"],[2,3,1,"","MultipleObjectsReturned"]],"stream.exceptions":[[3,3,1,"","InvalidAudioFileException"],[3,3,1,"","NoStreamAvailableException"]],"stream.models":[[3,1,1,"","AudioFile"],[3,1,1,"","Stream"],[3,1,1,"","StreamInstruction"],[3,1,1,"","StreamPoint"],[3,1,1,"","StreamVariable"],[3,1,1,"","TextToSpeech"]],"stream.models.AudioFile":[[3,3,1,"","DoesNotExist"],[3,3,1,"","MultipleObjectsReturned"]],"stream.models.Stream":[[3,3,1,"","DoesNotExist"],[3,3,1,"","MultipleObjectsReturned"]],"stream.models.StreamInstruction":[[3,3,1,"","DoesNotExist"],[3,1,1,"","InstructionState"],[3,3,1,"","MultipleObjectsReturned"]],"stream.models.StreamInstruction.InstructionState":[[3,2,1,"","from_sc_string"]],"stream.models.StreamPoint":[[3,3,1,"","DoesNotExist"],[3,3,1,"","MultipleObjectsReturned"],[3,2,1,"","send_stream_instruction"],[3,2,1,"","speak_on_stream"]],"stream.models.StreamVariable":[[3,3,1,"","DoesNotExist"],[3,3,1,"","MultipleObjectsReturned"],[3,2,1,"","send_to_sc"]],"stream.models.TextToSpeech":[[3,3,1,"","DoesNotExist"],[3,3,1,"","MultipleObjectsReturned"],[3,1,1,"","VoiceNameChoices"],[3,2,1,"","create_from_text"]],gencaster:[[0,0,0,"-","asgi"],[0,0,0,"-","distributor"],[0,0,0,"-","schema"],[0,0,0,"-","settings"]],osc_server:[[6,0,0,"-","exceptions"],[6,0,0,"-","models"],[6,0,0,"-","server"]],story_graph:[[2,0,0,"-","engine"],[2,0,0,"-","markdown_parser"],[2,0,0,"-","models"]],stream:[[3,0,0,"-","exceptions"],[3,0,0,"-","models"]]},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","exception","Python exception"],"4":["py","function","Python function"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:exception","4":"py:function"},terms:{"0":[3,7],"1":7,"1000":2,"10000":[2,7],"10200":7,"127":7,"150m":10,"2":2,"22":7,"2430":0,"255m":7,"3000":7,"3001":7,"300m":2,"301":7,"4":2,"404":7,"443":7,"4g":7,"5":3,"50000":7,"5432":7,"57120":7,"57130":7,"60000":7,"8":7,"80":7,"8081":7,"8088":7,"8089":7,"8090":7,"abstract":0,"boolean":6,"break":2,"case":3,"char":2,"class":[0,2,3,6],"default":3,"do":2,"enum":6,"function":[0,2,3,5,10],"long":6,"new":[0,3,6,7],"public":[2,3,6],"return":[0,2,3,6,7],"static":6,"super":0,"switch":[0,2],"true":3,"var":[2,7],A:[0,2,6,7,9],As:[0,3,6,7],For:[0,7],If:[2,3],In:[0,2,6,7],Is:2,It:[0,3,5,7],No:3,ONE:7,The:[2,3,5,6,7,9,10],These:2,To:7,Will:[2,6],With:2,_:0,__init__:[0,2,6],abl:6,about:[2,10],about_text:2,accept:[3,6],access:[0,2,7,9],access_log:7,acknowledg:6,acknowledge_handl:6,acreate_entry_nod:2,across:0,act:[2,3,7],action:[0,6,7,10],activ:7,add:[2,5],add_break:2,add_edg:0,add_head:7,add_nod:0,addit:[3,4],additional_channel:0,address:6,adjust:7,after:10,aget_entry_nod:2,all:[0,2,3,5,7,10],allow:[0,2,3,5,6,7,9,10],also:[0,2,3,5,7,10],although:0,an:[0,2,3,5,6,7],ani:[2,3,6,7,10],anymor:2,anywher:7,api:[3,12],app:[0,2,3,6],applic:6,ar:[0,2,3,6],arg:[0,2,3],asav:2,asgi:0,asset:0,assign:[2,3],associ:[2,3,6],assum:2,async:[0,2,3,6],asyncgener:2,audio:[0,2,3,10],audio_cel:[2,3],audio_cell_input:0,audio_fil:[0,2,3],audiobridg:3,audiocel:[0,2,3],audiofil:[0,2,3],authent:6,authstrawberrydjangofield:0,auto:3,auto_gener:3,automat:3,avail:[0,3,6],back:[0,4,6,7,9,10,12],backend:[0,3,5,6,7,10],background:2,base:[5,10],beacon:[3,6],beacon_handl:6,becaus:[2,3,7],becom:2,been:[2,10],behavior:3,better:0,between:[2,4],block:2,blocking_sleep_tim:2,bool:[2,3],booleanfield:[2,3],bracket:3,browser:10,build:9,bulk:2,c:2,cach:3,call:[0,2,3,10],callback:[0,6],can:[0,2,3,6,7,9,10],canva:[0,2],care:[3,5],caster:[4,7,10,12],cell:[0,2,3],cell_cod:2,cell_ord:2,cell_typ:2,celltyp:2,certain:0,certbot:7,challeng:7,chang:[0,2],channel:0,charact:[2,3],charfield:[2,3],charset:7,check:[3,6],choic:[2,3],choos:2,citizen:2,classmethod:3,clear:2,click:3,client:[3,6],client_address:6,client_max_body_s:7,close:0,cloud:3,cluster:6,cmd:6,code:[2,3,5,6],collect:[0,2,3],color:2,com:3,comment:7,commun:[3,4,5,6,7],concept:[2,14],concern:0,conf:7,config:[1,5,7],configur:0,connect:[0,2,5,7,12],consid:[0,2,3],consist:[2,10],constraint:3,contain:[2,7],content:[0,2],context:2,control:[2,3,7],convers:3,convert:[2,3],copi:3,core:2,could:[2,7],count:3,counter:3,cover:2,cpu:7,creat:[0,2,3,6,10],create_entry_nod:2,create_from_text:3,create_script_cel:0,created_d:3,creator:2,curli:3,current:3,cycl:2,data:[3,9],databas:[0,3,5,6,7],date:3,datetimefield:3,de_neural2_c__femal:3,de_standard_a__femal:2,de_standard_b__mal:2,decod:0,decor:0,defin:[0,2],definit:6,delet:0,delete_edg:0,delete_nod:0,delete_script_cel:0,deploi:[5,7],deploy:[5,10],describ:[2,4],descript:3,design:6,detail:0,determin:0,determinist:2,dev:[5,7],develop:[5,7],dhparam:7,dialect:2,dict:2,differ:[0,2],difficult:[0,2],directli:7,disconnect:0,discov:6,displai:2,display_nam:2,distribut:10,distributor:[1,5],django:[3,5,6,7,10],django_nam:0,doc:[2,3],docker:[0,10],document:[7,9],doe:[0,2,6],doesnotexist:[2,3],don:0,due:3,dure:2,dynam:10,e:[0,2,3],each:[2,3,6],easier:7,easili:2,edg:[0,2],edge_uuid:0,edit:[2,10],editor:[2,4,5,7,10,12],email:0,emphasi:2,empti:[2,3],encount:2,end:2,end_text:2,endpoint:[0,3],engin:5,entri:2,entrypoint:2,enumer:2,environ:0,error:7,error_log:7,error_messag:0,etc:7,eval:2,eval_python:2,even:10,everi:[2,3],exact:3,exampl:[2,3],except:[0,1,2,5,6],exec_python:2,execut:2,execute_audio_cel:2,execute_markdown_cod:2,execute_nod:2,execute_sc_cod:2,exist:[2,3],experi:10,explicit:2,extend:2,extern:3,factori:0,fail:6,failur:6,fallback:2,fals:[2,3],favicon:7,femal:2,field:[2,3],file:[2,3,5],filefield:3,filter:3,find:[0,3],finish:[3,6],firewal:7,first:[2,3],first_nam:0,floatfield:2,flow:[2,12],foo:[2,3],foobar:2,force_new:3,foreignkei:[2,3],form:6,format:[2,3],forward:7,frame:0,framework:10,free:7,from:[0,2,3,6,7,9],from_sc_str:3,front:[4,7,10,12],frontend:[2,5,7,9,10],fullchain:7,g:[0,2,3],gain:5,garbag:3,gc:2,gencast:[1,2,3,5,6,7],gencasterchannel:0,gencasterrender:2,gencasterstatusenum:6,gencastertoken:2,gener:[0,3,5,10],get:[3,6,9],get_stream_vari:2,getter:2,given:[0,3,6,10],global:12,goal:6,googl:3,gp:10,gql:5,grant:10,graph:[0,1,7,10,12],graphdetailtempl:2,graphiql:0,graphql:[0,5,9,12],graphql_check_authent:0,graphql_nam:0,graphqlwsconsumerinjector:0,graphsess:2,graphupdatemessag:0,group:0,gstreamer:3,gunicorn:6,ha:[2,3,6],halt:2,hand:0,handel:5,handl:[2,3,5,6,10],happen:[2,3],have:[0,2,6,10],hello:2,help:3,helper:0,here:[0,3],hex:2,hit:6,hold:2,host:[3,6,7],hostnam:3,how:[2,3],http:[3,7],http_upgrad:7,human:[2,3],ico:7,id:3,identifi:3,implement:[2,3],implicit:2,in_edg:2,in_nod:2,includ:[6,7],indefinit:2,info:0,inform:7,initi:7,inject:0,inlin:2,input:[3,6,10],insert:7,instanc:[3,6,7],instead:3,instruct:3,instruction_text:3,instructionreceiv:3,instructionst:3,integ:6,integerfield:[2,3],interact:[3,7],intern:3,introduc:[3,7],invalid:3,invalidaudiofileexcept:3,ip:[3,6,7],is_act:0,is_blocking_nod:2,is_entry_nod:2,is_staff:0,isauthent:0,iter:2,its:[0,2,3,6],janu:[3,6,10],janus_in_port:[3,6],janus_in_room:[3,6],janus_out_port:[3,6],janus_out_room:[3,6],janus_public_ip:[3,6],jaun:3,javascript:9,job:3,jump:2,kei:[2,3],know:3,known:2,kwarg:[0,2,3],lack:7,lang:6,lang_port:6,languag:[2,3],last:3,last_liv:3,last_nam:0,latenc:10,layer:0,layout:6,less:5,letsencrypt:7,level:[0,2],like:[3,7],linear:10,list:[0,2],listen:[3,7,10],littl:2,live:[3,6,7,10],local:[3,5,6],locat:7,log:[0,7],log_not_found:7,loggin:0,loginerror:0,look:[2,7],loop:2,low:10,machin:7,made:[0,2],mai:2,make:[3,5,6],male:2,malformedoscmessag:6,manag:[2,3,5,6,7,10],mani:2,manner:[0,2,6],manual_finish:3,map:6,markdown:5,markdown_pars:2,match_obj:2,max_step:2,mayb:2,md:2,md_to_ssml:2,me:2,media:0,memori:7,messag:[0,3,6,7],metadata:[0,3],method:[2,6],microphon:10,missingchannellay:0,mode:7,model:[0,1,12],moder:2,modern:10,modifi:3,modified_d:3,modul:0,more:[0,5,7],most:3,mount:3,move:0,mozilla:7,msp:2,multipl:[2,3,10],multipleobjectsreturn:[2,3],multitud:2,music:[2,10],mutat:0,n:2,naiv:6,name:[0,2,3,6,10],nat:7,nativ:[2,6],ndef:3,necessari:[3,4,6,7],need:[0,2,3,7],network:7,new_edg:0,new_nod:0,ngingx:10,nginx:7,nice:0,node:[0,2],node_upd:0,node_uuid:0,nodeupdatemessag:0,nois:3,non:[3,10],none:[0,2,3,6],nostreamavailableexcept:3,now:[0,2],num_listen:3,number:3,object:[3,6],obsolet:0,obtain:[2,9],off:7,older:6,onc:2,one:[2,3],ones:0,onetoonefield:2,onli:[2,6,7],oper:5,option:[0,7],order:[2,6],org:7,origin:7,orm:6,osc:[3,5,7,12],osc_arg:6,osc_backend:7,osc_backend_host:6,osc_backend_port:6,osc_serv:6,oscauthmixin:5,oscbackendauthexcept:6,oscserv:6,other:2,otherwis:7,our:[0,2,3,6],ourselv:3,out:[2,3,6,7],out_edg:2,out_nod:2,over:2,overflow:0,own:[2,6],page:0,pair:3,paramet:[2,3],pars:2,parser:5,part:0,pass:3,password:6,past:3,peer:7,pem:7,per:2,permiss:10,plai:2,playback:[2,3],playbackchoic:2,plu:2,plugin:0,point:[2,3],polici:2,poll:6,port:[3,6,7],posit:[2,10],position_i:2,position_x:2,possibl:[3,7],postgr:7,primari:[2,3],prioriti:7,privkei:7,probabl:0,process:6,product:0,program:2,project:0,propag:7,proper:[5,7],properli:6,properti:[2,6],proto:7,protocol:[4,5,6],protocol_vers:6,provid:2,proxy_add_x_forwarded_for:7,proxy_http_vers:7,proxy_pass:7,proxy_redirect:7,proxy_set_head:7,pub:7,public_vis:2,publish:0,pure:2,purpos:0,python:[2,10],python_nam:0,pythonosc:6,queri:[0,5],quickstart:10,radiophon:10,rais:2,raise_except:2,rate:3,rather:[6,7],raw:[2,6],raw_ssml:2,reachabl:3,react:10,readi:6,real:[7,10],realtim:7,receiv:[0,3,6,7],recurs:2,redi:7,redirect:7,refer:[2,7],regard:[0,7],reject:6,relat:[2,3],relationship:[2,3],releas:3,reli:7,remot:6,remote_action_handl:6,remote_addr:7,remoteactionmessag:5,remoteactiontyp:6,renam:0,render:10,replac:[0,2],repres:[2,3],request:6,request_uri:7,respect:[2,3],respons:2,restrict:[0,6],result:[2,6,7],return_valu:[3,6],reusabl:0,revers:[2,3],robot:7,room:[3,6],rtp:3,run:[0,2,3,6,7],sai:2,same:3,sampl:3,save:2,sc:3,sc_name:3,sc_string:3,scacknowledgemessag:[3,5],scbeaconmessag:5,schema:[1,5],scheme:7,score:2,scratch:2,script:2,script_cel:2,script_cell_input:0,script_cell_uuid:0,scriptcel:[0,2,3],scriptcelltimeout:2,scsynth:3,search:3,see:[0,2,3,5,6],seem:[3,6],self:3,send:[3,6],send_stream_instruct:3,send_to_sc:3,separ:3,serv:3,server:[0,3,5,7,12],server_nam:7,servic:[3,5,10],session:3,set:[1,2,3,5],setup:2,share:3,signal:3,singular:2,slug:2,slug_nam:2,slugfield:2,so:[0,2,3,6],solut:3,solv:3,some:[6,7],someth:2,something_unknown:2,sound:[5,7,9,10,12],sourc:[0,2,3,6],speak:[2,3,6],speak_on_stream:3,speaker:2,specif:0,speech:3,split:0,sqlite:0,ssl:7,ssl_certif:7,ssl_certificate_kei:7,ssl_dhparam:7,ssml:[2,3],ssml_text:3,stack:0,start:[2,3],start_text:2,state:[2,3],stateless:3,statement:[2,3],statu:[6,7],step:4,still:2,storag:5,store:[2,3,6],stori:[1,5,7,10],story_graph:[0,2],str:[0,2,3],strawberri:0,stream:[1,2,5,6,7,9,10],stream_assignment_polici:2,stream_point:[0,3],stream_to_sc:3,stream_vari:[0,2],streamassignmentpolici:2,streaminstruct:[2,3,6],streampoint:[2,3,6],streamvari:[2,3],string:[2,3,6],sub:7,subscrib:0,subscript:0,success:6,supercollid:[2,3,6,7,10],support:7,surround:[2,3],sync:2,synth:6,synth_port:6,t:0,tag:2,take:[2,3,5],talk:2,target:6,templat:[2,12],template_nam:2,term:6,test:5,text:[2,3],textfield:[2,3],texttospeech:[2,3],than:7,thei:[2,3],them:[0,7],therefor:2,thi:[0,2,3,5,6,7],thing:0,through:[2,5],time:[0,10],tool:0,topic:7,trace:3,trade:5,traffic:7,transform:2,transmit:3,treat:2,trigger:6,tweak:10,two:2,txt:7,type:[0,2,3,5,6],typescript:5,u:0,udp:[5,6,7],ufw:10,ui:2,under:[0,3],understand:6,uniqu:2,unlock:3,unset:0,updat:[0,3,6],update_audio_fil:0,update_nod:0,update_or_create_audio_cel:0,upgrad:[6,7],upload:3,url:2,us:[0,2,3,4,5,6,7,10],use_input:[3,6],user:[0,3,7,10],usernam:0,uses:6,utf:7,uuid:[0,2,3,6],uuid_to_group:0,uuidfield:[2,3],v6:7,val:3,valid:[2,3,6],validate_gencaster_token:2,valu:[2,3,6],variabl:[2,3],varieti:2,version:6,via:[0,2,3,6,7,10],visibl:2,visual:2,voic:3,voice_nam:3,voicenamechoic:[2,3],volum:2,vue:10,wai:[2,7],want:2,we:[0,2,3,5,6],web:10,webrtc:[3,7,10],websocket:0,websocket_disconnect:0,well:[0,2],what:2,when:[0,3,6],where:[2,3],which:[0,2,3,5,6,7,9,10],within:[2,3],without:3,word:2,work:6,world:2,would:[0,6],write:5,written:[2,5,10],wrong:6,x:[2,7],y:2,yet:[0,2],you:[0,2]},titles:["GenCaster config","API","Story Graph","Stream","GraphQL","Caster back","OSC Server","Deployment","Caster editor","Caster front","Gencaster","Quickstart","Services","Caster sound","Story Graph"],titleterms:{add:4,api:[1,5,6],back:5,base:0,caster:[5,8,9,13],config:0,connect:9,content:[1,10,12],deploi:0,deploy:[0,7],dev:0,develop:0,distributor:0,docker:7,editor:8,engin:2,except:3,flow:9,front:9,gencast:[0,10],global:5,graph:[2,3,5,14],graphql:4,local:0,markdown:2,model:[2,3,5,6],ngingx:7,osc:6,oscauthmixin:6,parser:2,queri:4,quickstart:11,remoteactionmessag:6,rout:6,scacknowledgemessag:6,scbeaconmessag:6,schema:0,server:6,servic:[7,12],set:0,sound:13,stori:[2,14],stream:3,templat:9,test:0,todo:[0,2,3,4,6,11,14],ufw:7}})