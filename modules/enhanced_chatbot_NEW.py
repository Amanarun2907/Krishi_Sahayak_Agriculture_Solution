import streamlit as st
ion")
ion/js"applicat, e}.json"{sector_namchat_a, f"", datloadon("📄 Down_buttoad.downl         st)
   default=str, indent=2, te[chat_key]ion_stas(st.sessumpn.dta = jso     da:
       ")or_name}ctr sey ounique_ke=f"export_{ort", key Expbutton("📋if st.       col2:
  th
    wi st.rerun()       = []
    e[chat_key] ession_stat        st.s    :
r_name}")or sectoey r_{unique_kleaey=f"cChat", kear "🗑️ Clbutton(f st. i1:
        with col
   (2)t.columns = sol21, c
    col buttons # Control   
   "
    )
 iculture...agrng about "Ask anythilaceholder=,
        pe_submitdln_change=han,
        otor_name}" or secnique_key_{uuthat_inp key=f"c   ..",
    r.nteess Etion and prur ques"💬 Type yo
        xt_input(
    st.tebackth callt field winpu   # I 
 "
   e}"] = "ctor_namr se_key o{uniqueinput_e[f"chat__stat.session      star input
  # Cle      
      
    
        })w()tetime.no: da'timestamp'  
          : response,   'content'      t',
   sistanrole': 'as           '
 d({key].appent_state[cha.session_  stnse
      # Add respo   
             y again."
se trleatr(e)}. PError: {sonse = f" resp            as e:
pt Exceptionxce        eer_input)
response(ust.generate_tboponse = cha        res        ]
or_name}"tbot_{sectional_cha"foundat_state[f= st.session    chatbot             lChatbot()
oundationa = AdvancedF_name}"]ectortbot_{stional_chaoundae[f"fon_stat st.sessi           
        ate:_stsionst.ses" not in }tor_nameot_{secchatbal_foundation   if f"          else:
               t
conten[0].message.oicesetion.ch chat_complonse =esp     r
                   
             )        =1500
   tokens      max_              ,
e=0.7  temperatur                 t",
 nstan-i-8b.1ma-3odel="lla       m          ,
     ]           
       ssage}_mentextntent": cor", "co"use:    {"role"             
        em_prompt},ent": systnt", "co "system{"role":                        messages=[
                    s.create(
ionchat.completon = client.completi     chat_      
                    _input
  else user_contextif analysisput}" {user_intion: nQuesxt}\n\ontes_cysialalysis: {an = f"Anext_message cont           
                t)
    ien_clt=httpp_clien_KEY, htty=GROQ_API_ke= Groq(api    client            
 t=30.0)lse, timeounv=Faust_ex.Client(tr = httphttp_client              ")
  nt.sistatural asl agricul helpfure ae, "You anamctor_(se.getT_PROMPTSHATBOm_prompt = Cte  sys             
               
  mport Groqom groq i      fr   px
       httport   im         I_KEY
     GROQ_APOT_PROMPTS, import CHATBg   from confi        
      i:   if use_ap        
 try:        se
 respon # Generate  
        })
           w()
  .nome datetitimestamp':          '_input,
  serent': u'cont       
      'user',  'role':        
  ({_key].appendn_state[chat   st.sessio
      messaged user        # Ad
        
eturn        r   t:
 r_inpuif not use()
         "").strip}", sector_name_key or{uniqueut_(f"chat_inpn_state.getessio st.st =user_inpu        
t():e_submiandlf hLOAD
    deREGE k - NO PAlbach calat input wit
    # Chrue)
    w_html=Tnsafe_allo u""",               </div>
                 >
]}</divnt''conte">{message[6;ght: 1.ne-hei2d2d2d; lie="color: # styl     <div               g><br>
ak:</stronhayn} Krishi Sat_icochatbo;">{: #1b5e20e="colorg styl <stron                   
af50;"> solid #4cft: 4pxborder-le                       
     5rem 0; gin: 0. mardius: 15px;der-ra1rem; borng:       paddi                   ); 
   0%#c8e6c9 100fff0 0%, deg, #fradient(135nd: linear-gbackgrouiv style=" <d        "
       down(f""     st.mark   
            else:)
        w_html=Truee_allounsaf    """,                </div>
       n>
      ]}</spaontent'ssage['c">{meor: #2d2d2d;tyle="col <span s                  br>
 rong></st You:<d47a1;">👤lor: #0"cog style= <stron             ">
       #2196f3;solid: 4px eft   border-l                   
       : 0.5rem 0;5px; marginr-radius: 1rem; bordedding: 1 pa                           %); 
b 100d 0%, #bbdef #e3f2f(135deg,gradientd: linear-"backgrounv style=di  <            ""
  kdown(f"st.mar                er':
e'] == 'usessage['rol      if m:
      chat_key]ssion_state[ in st.semessager 
        fo
    else:started!")low to get  bea messageet. Type ssages y"💬 No me.info(      st== 0:
  ey]) chat_ke[ssion_statlen(st.se
    if storylay chat hiisp# D 
    e)
   _html=Trusafe_allowun """,  </div>
     </p>
      
   key])}[chat_ssion_state {len(st.ses:ge| Messady  Rea   Status: 🟢        ;">
 margin: 0rem; -size: 0.9nt_color}; fo: {statusolorn: center; c"text-aligyle=      <p stp>
     </     ything!
 an- Ask me).title()} ace('_', ' 'ame.repl{sector_nzed in peciali      S>
      : 1rem;"ombottargin-66; molor: #6er; centalign: cext-="tle    <p sty>
            </h3t
stan} Assiatbot_type {chhayakhi Sa} Kristbot_icon      {cha">
      nter;ign: cet-alm; texottom: 1rer}; margin-bolo_ctatuscolor: {sh3 style=">
        <0,0.1);"x rgba(0,0,: 0 8px 25phadow}; box-stus_color solid {stader: 2px  bor           0; 
    : 1rem5px; margin-radius: 1; bordering: 1.5remdd pa               ; 
e9ecef 100%) 0%, #eg, #f8f9faent(135dr-gradid: lineaunackgrole="b<div sty""
    n(f"t.markdow7D"
    s "#6C75_type elsetbothaAPI" in c" if "B57r = "#2E8tatus_colo sg
   rface stylin# Chat inte  
    
  "t_icon = "🧠  chatbo     "
 tional AI = "Founda_typehatbot    ct()
    tbondationalChadFou"] = Advanceme}t_{sector_natbonal_chaf"foundatioion_state[esst.s    s      state:
  session_ in st.otname}" nbot_{sector_tional_chat f"founda      ife:
  "
    els = "🤖ot_icontb   cha
     Powered"= "API-type  chatbot_  KEY
     rt GROQ_API_g imponfi   from co    use_api:
 if 
    alizationt initi  # Chatbo
   = []
    at_key]ion_state[ch  st.sess
      :on_statein st.sessikey not chat_ if    
   "
 ctor_name}_history_{sef"chatey = chat_k
          else:_key}"
  ry_{uniquechat_histo"at_key = f  ch     
 e_key:uniqu
    if stancesinbot t chatte differen to separaunique key
    # Use 
    """page
    oad the reldoesn't ce that interfaat N: Create chED VERSIO"
    FIX ""   = None):
_key: str rue, uniquepi: bool = Te, use_a: str = Nonsis_context str, analye:ctor_namnterface(seate_chat_i

def creces.")
 experienditions andocal con on lbasedactices  pr farmingurting yog and adapninKeep lear, "goryips.get(cate  return t    
         }
         ives."
 or cooperat groupsoin farmers. Jence experiledge andowre knhao sea t your arr farmers inh othetwork witNeing": "neral_farm    "ge     .",
   ubsidies and semesscht overnmenon gormation  latest infthe) for  Kendra (KVK Sahayak Krishi your local: "Visitchemes"vernment_s  "go        
  ",recasts. for apps foreathee w. Usesvititi farming acanplatterns and ack po trr diary ta weathe": "Keep teclimaher_at       "we     .",
eser resourcwatnd  your soil aConsidercrops. hoosing ing before c and pricd demanderstanets to und markt localn": "Visiselectioop_  "cr     
     arison.",s for comporttest repeep soil H. Kd prtility ananges in feo track ch tyears-3 y 2st soil evernt": "Tenageme "soil_ma           ,
rately."els accumoisture levl  soiornit moe tore probtuor soil moisensiometer e tUse a simpl": "gationri    "ir     .",
    timingrbicideroper he p. Usece disturban soileseducull and rr to p it's easieist -l is mohen soi "Weed wment":agean    "weed_m     ",
   nitoring. for mo trapsheromoneUse ppesticides. um trroad-specoiding btors by avl predarage natura "Encout":managemen  "pest_        ,
  rly."blems eap detect pro visits helieldlar f. Regu diagnosisfor betternd soil d plants afecteos of afhote p": "Tak"crop_health           {
   tips = ""
      ories"ecific categ tips for sphelpful""Get 
        ":> strry: str) -self, categoul_tips(lpft_he def _ge  ""
    
     return   
    ")
      thl heality and soi sustainabilermong-t improve lracticesng pic farmiry, "Organ(categoice.getorganic_adv  return 
                  }nts"
    equiremegation rrid reduces irure anl moistserve soi helps conching"Organic mul": "irrigation        
        ethods",ntrol manic weed coctive orgng are effeual weedind mantation, aop roMulching, crgement": "naeed_ma     "w        
   ",ethodsl mrost contnic peve orgare effectis aontrol agentlogical cbiond c extract, ali, garoil": "Neem ntmanageme  "pest_              th",
soil healle or sustainabertilizers fbioft, and vermicomposke compost, s liertilizere organic fUsth": ""crop_heal          {
      e = nic_advic    orga      _lower:
  nput" in user_i"naturalor ut_lower inpr_" in use"organic    if            
 puts")
tural incul agriallfor analysis efit  cost-benidernsCo, "egory.get(catcost_advicen ur        ret         }
 0%"
      ield by 20-3es yncreas and i30-50% watersaves ut /hectare b0,00000-8,0₹50tion costs  irriga "Dripon":irrigati         "     
  ",ctare00/he1000-20t ₹s cosdere, herbici0-3000/hecta₹200costs l weeding ": "Manuagementnama     "weed_           ontrol",
e ctiving effec maintain0% whilets by 30-5de cossticireduces peM ": "IPmanagement "pest_              ",
 stsertilizer con f000 ives ₹5000-10ple but saam0-1000 per scosts ₹50il testing Soh": "lt "crop_hea              dvice = {
   cost_a   er:
       _lowser_input in u"expensive"_lower or _inpute" in userr or "pricr_input_lowen usest" i  if "co
           
   ower()r_input.lwer = useput_loinser_
        u"""n user inputbased odvice tual antex co"Get        ""
r:) -> ststr, category: put: strer_in, us_advice(selftextualconf _get_de
     ""
        return 
        s[0]]
   sueentioned_is_info[mrn detailed retu  :
         led_info in detaiues[0]oned_isses and mentiioned_issu  if ment   
   
        _lower] user_inputue inssues if isssue in isue for isssues = [ismentioned_i    
    "borer"]hitefly", ", "w"aphid"zinc", "iron", ", sru", "phospho"potassiumen", nitrogs = ["ue
        issfic issuesspeciheck for # C 
        
       ")"ops[0], tioned_crmenet(rop_info.gn cretur          
       }     
  "cyefficienor ion fip irrigatuse drarvesting, ar h, regult irrigations frequenreequie": "Regetabl  "v            nths",
  2-18 mor 1 afteestn, harvioavy irrigatrequires heuary-March, ebr"Plant in Fe": can"sugar               70%",
 lls open 60-hen boest wons, harvrigati10 irrequires 8-May, l-nt in Apri"Plaon": ttco  "          n",
    rowhusk turns bt when harvesrrigations, quires 6-8 ix25 cm, reing 60"Plant spacmaize":           "   25%",
   20-sture is n moigrairvest when  hans,igatios 4-5 irrireember, requNovOctober-: "Sow in  "wheat"            ture",
   -35% moisat 30s, harvest 25-30 dayplanting at ter, transding wastaninches s 2-3 equire"Rrice":           "      
fo = { crop_in     ops:
      mentioned_crf       i        
  put_lower]
n user_in crop i in crops ifopr crp fos = [crotioned_crop   men"]
     onato", "oni"pot"tomato", table", vege", "rcane", "suga"cottonze", aiwheat", "mrice", ""rops = [
        centionsfic crop m for specieck       # Ch    
 , {})
    o"ed_inftail"deget([category].ge_basewled= self.knofo ailed_in    det    lower()
input. = user_put_lowerr_in  use""
      nput"r id on usetion baseic informat specif    """Ge
     str:->) gory: strate str, c user_input:on(self,_informatit_specific    def _ge 
arts)
   esponse_p".join(r\neturn "     r      
   ils")
  ific detaore spece provide m0%}) - Pleasdence:.fionl:** Low ({c Levecenfiden\n❓ **Co(f"pend_parts.apesponse    re:
          els
      ")nce:.0%}) ({confideel:** Mediumdence Lev️ **Confipend(f"\n⚠se_parts.apespon     r    :
   0.4ce > if confiden      el")
  })nce:.0%confidel:** High ({ce LeveidenConf **f"\n✅d(.appenartssponse_pre           0.7:
  ce >nfiden    if co
    e indicatoronfidenc # Add c          
   tips}")
  ro Tip:** {f"\n🌟 **Pend(appts.se_parrespon          ps:
  f ti 
        i")
       e}ual_advicextont\n{cce:**Advidditional  **A(f"\n💡s.append_part   response   
      _advice:ntextual if co  
       
      c_info}")\n{specifin:**Informatioific n📋 **Spec\.append(f"nse_partspo   res    nfo:
     pecific_i      if s       
  esponse]
  [base_r =sponse_parts
        rese all part Combin  #      
        tegory)
s(ca_tip_helpful._getelf   tips = s    ips
 l t helpfu   # Add    
     
    ry)put, categovice(user_inal_adontextulf._get_c sevice =_adntextual   codvice
     extual a cont   # Add    
         ry)
ego_input, cattion(userc_informaecifilf._get_sp seo =c_infcifi      spermation
   infoficd speci        # Ad   
  onses)
   spce(rerandom.choionse = se_resp  ba      
onses"]gory]["respe_base[cate.knowledgs = selfresponse   e
     responsse  ba       # Get   
 t)
     inpuory(user_eg_catstf.find_bee = sely, confidenc    categor    ut"""
ser inpsed on ue baresponsive mprehens coerateGen    """> str:
    put: str) -in, user_lfesponse(seerate_r gen  
    defidence
   conftegory,best_ca    return      1.0)
eywords"]),["kry]best_categobase[f.knowledge_sel/ len(core (best_sence = minonfid     c      
   ory
  eg catategory =     best_c           = score
 core   best_s         ore:
    > best_scscore   if         er)
  _lowput in user_inword if keywords"] data["keyinor keyword  f sum(1core =         s:
   items()_base.owledgeelf.knin s, data egoryor cat     f    
       0
 t_score =      bes"
  rmingneral_fay = "get_categor        bes.lower()
nput user_iut_lower =    user_inp"""
    e scoreidenc confgory withhing catet matche bes"Find t"        " float]:
uple[str,tr) -> Tr_input: self, use(scategoryind_best_ def f
    
   
        }     }        }
              redit"
  access to cing, sharwledgeng, knohasi purculkprices, b"Better : "erativesarmer_coop  "f                s",
  ence, yieldst incidpes, weather, , outputrack inputseping": "Tked_cor       "re         y",
    diversiton, bioservatier conat farming, worganicrotation, : "Crop ices"ctinable_pra    "susta                nfo": {
tailed_i  "de        
            ],          asing."
purchugh bulk s throstut coreduce inpprices, and cess better dge, ace knowleshar to esrativr coope omer groupsaroin forks:** Jr Netw🤝 **Farme      "            ",
  .-makingr decisiontteor be fdsheetse spreas or simplgement appm mana Use far practices.y profitableifto ident, and costs , yieldsTrack inputsg:**  Keepin **Record"📊                    
h.",tal healtironmenity and envbilprofitag-term ve lonces improese practi. Thagementanted pest mintegra and ilizers,c ferton, organitatiop ro Use cre Farming:****Sustainabl        "🌱        
     ses": [espon     "r        ,
       ]       
     hnology""tecion", cis", "preorganic", "nability", "sustai "income                   profit", 
eld", "", "yi "croprmer", "faure",, "agriculting"     "farm      [
         ywords": "ke                ng": {
al_farmi   "gener  ,
          }}
                       owing"
   snd preventedd loss avers yielred. Co sum insu-2% ofremium: 1.5nce": "Pop_insuracr   "                
 ",erttnic ma, orgautrientson, micrsts pH, NPKars. Te3 yeery e ev "Fre":ealth_cardsoil_h        "          
  res",o 2 hecta tlding uplity: Landho Eligibits.3 installmen/year in 6,000": "₹isan "pm_k                  ": {
 iled_infoeta"d                
      ],     s."
     seasepests, di, flood, to droughtoss due  yield lverst. Conmenzed by goverdiubsiremium ses. Ped lossher-relatt weatts agains** Protecnce (PMFBY):*Crop Insura️ *   "🛡                 s).",
as (KVKgyan KendrKrishi Vible at nts. Availaendmeand soil amilizers  for fertonsmmendaticovides re. Provery 3 yearsil testing e soCard:** Free Health il"📋 **So                   ",
 counts.o bank ac ttransferfit ect benents. Dirinstallmes in three al farmerd marginsmall anear to ₹6,000 per yvides :** Proisan Scheme**PM K🏛️    "               : [
  "responses"              ],
         "
         UMKUS", "Yr", "PMFB "fertilizerd",il health ca"so                    n", 
"PM Kisae", , "insuranc "loan"dy",subsieme", "ch"s", ernment  "gov                ": [
  "keywords              
  ": {schemesvernment_      "go  },
               }
        "
         tolerant1 are flood- Sub-e Swarnarieties lik"Rice vaance": lood_toler   "f              
    crops",erantht-tolre droug, chickpea aorghumlet, sarl mil": "Peranceught_tole"dro                   ",
 5-30June 1: 5-31, Latey: May 1ne 1st, Earl onset: Jurmalt": "Nonseon_onsomo      "             fo": {
 tailed_in "de             ],
          
        ges."iting sta and frug floweringcially durinops, esperess cr stanges can chdity. Suddenl, and humialre, rainftuerampck te** Tra Monitoring:*Weather"📊 *                  asts.",
  forecon weather dates based nting st pla adjuques, andation technirvnsees, water corietiistant varought-res. Use d patterns rainfallge affectsanlimate chptation:** Cate Adalim **C   "🌡️           
       mustard.",at,ops: wheonsoon crLate mze.  rice, maips:onsoon cro m. Earlypatternsnsoon  moundroalendar a cropping canns. Plon raimonso on s heavilyture dependiculndian agrgement:** Isoon Mana"🌧️ **Mon               
     ": ["responses                 ],
             on"
  daptati", "a changelimateon", "cd", "seaslooht", "fug "dro                  on", 
 "monso, erature"l", "tempnfal", "rai", "climateeather "w                ": [
   words       "key
         {imate": ther_cl   "wea
         },                }
        une)"
    h-Jarc cucumber (Melon, waterms,bleeta"Veg": rops "zaid_c          
         ch)",ober-Mar(Oct potato pea,chickmustard, at, barley, ": "Whes_crop    "rabi               ",
 e-October)an (Junsoybeoundnut, garcane, gr, suttonmaize, co, ": "Riceif_crops      "khar           ": {
   iled_info  "deta            ],
                 sify."
  diverllynd gradua aliar with're fami youth cropswi. Start e management mort requiretable bun be profind spices caetables aops like veg-value cr Highability:**Profit**        "💰         
    dnut.",n-grounheat, cottooybean-wmaize-sses, ce-wheat-pulotations: riity. Good rtiler soil fand improveles yck pest crops to breaate cn:** Rotrop Rotatio🔄 **C   "                .",
 d soilswell-draineses prefer y soils, pullaell in c wows grnce. Riceur experied yomand, andearket ability, m water availe,imat cloil type, sonops based oose cr* Cha:*eriCrit Selection **Crop🌾      "              
 ": [nses     "respo          ],
             g"
    oppin, "intercr""rotationtability", profi"d", deman"market                  
   ", l typeate", "soiimcl", "eason", "sarietyon", "vrop selecti        "c            rds": [
     "keywo       ": {
    selectionrop_"c         },
               }
            
    "ructureo improve ster tganic mattAdd ors. diseaseand root gging aterlonts w preve drainageoodage": "G"drain                ,
    ally"e annuYM/hectaronnes F10-15 tsoil. Add in top3-5%  "Target c_matter":organi        "          ",
  .0-7.0ables: 6-8.0, Vegetton: 6.0-7.0, Cot.0 6eat:Wh.5-6.5,  5 "Rice:_ph":      "soil           
   d_info": {ile      "deta        ,
   ]             ally."
  e naturtructur soil simproves This ts.c amendmen organige and usingve tillassig exceinid avomicrobes bycial fims and beneorarthwage ey:** EncourtivitAccal *Biologi *  "🪱                
  t.", iowerlfur to lor suaise pH  to r.0. Use limepH 6.0-7refer crops p. Most teric matand organents, utri pH, nrs forea every 2-3 ysoil Test l Testing:***Soi"📊 *                   ntion.",
 tend water reertility, acture, fstrumprove soil  itolarly nure regud mayart or farmos Add comp matter.3-5% organicins y soil contath:** Healthl Healoi  "🌍 **S                 
 ponses": [es      "r     
             ],"
        thwormss", "ear"microbe", structurelth", ""tiainage",       "dr             
  ", "pH","manure",  "compostter",ganic maty", "or, "fertilitoil" "s                   ords": [
   "keyw             nt": {
ememanagoil_   "s                },
 }
                   ment"
 le to impleimpuse but ster waigh e. Hor ric method fTraditional "n":_irrigatio "flood                   or",
uces labredn, tiodistribum water Unifors. blegetaals and ve for cere": "Goodgationrier_irprinkl "s                 
  are",/hect80,0000,000-ost: ₹5es yield. Ceds, improv weducester, re: "Saves waation"rip_irrig         "d        fo": {
   inailed_"det            ],
                  ases."
   diseroott evenprto erwatering  ovdeep. Avoidches insture 2-3 oiCheck soil m growth. reducedrling, and  leaf cue wilting,includmptoms ent:** Sy Managemter Stress **Wa    "🌡️            ",
    ate timing.currs for acture senso moisrs or soilnsiometete Use nt.pmeruit develod fang  flowerins arecal periodage. Critith stgrowp ased on cro bng:** Watern Scheduli**Irrigatio"⏰                     city.",
capa% of field t 60-80re amoistun soil ps. Maintaind cash croruits, a fgetables, ve's ideal forn. Itatiorig irodred to floter compaes 30-50% wagation savDrip irriency:** on Efficiigatirr"💧 **I                  [
  nses":   "respo                     ],
       vation"
  ", "conserncy"efficie, ng" "schedulire", "moistudrought",   "         
        ", r stresswated", "", "flooklerprin"s", "dripg", erinattion", "w "irriga                   
 [eywords":        "k
        ation": {    "irrig,
                  } }
            "
     cropseaf broadlsy weeds in asr gr, MCPA foealsweeds in ceroadleaf 2,4-D for bricides": "e_herb"selectiv                   ",
 ive controlselectn- for nokg/hectare1-2 Glyphosate rowing. vely g are actien weedspply wh"Agence": emer    "post_               at",
 whed ice anfor rctare /he-1.5 kgdimethalin 1nce. Penmergeand weed e crop Apply beforee": "enc"pre_emerg              {
      ": iled_info    "deta          ,
      ]           "
 nt density.optimal plaies and rop varietetitive c. Use compdsess weeprng supchiand mulng ppitercroycles. In c weedkson breaCrop rotatiol:** tural Contr**Cul       "🌾             ",
 ns.tioel instruclabollow s feds. Alway we growingget 2,4-D) targlyphosate,icides (ence herbergemost-tion. Pinaed germrevent wee) pazinin, atrndimethalcides (pence herbie-emergeon:** Prtilecbicide Se "🧪 **Her                   ,
thods." chemical mecal, andchanicultural, me Combine r areas.rgell for las work weherbicidewhile arms, r small ftive foec is most effedingy. Manual weon is key interventi** Earlategy: Stragementan*Weed M "🌱 *                ": [
   ses"respon            ],
                  nnial"
  s", "pere", "sedgesy", "grasdleaf    "broa      
          stance",e", "resigenc-emerostgence", "pemer"pre- tion",peti  "crop com        
          ching", al", "mul", "chemic", "manualeding", "weicide", "herb  "weed           [
       ": ords    "keyw          ": {
  teneed_managem   "w          },
           }
          er"
      0.5ml/lit spinosad  with sprayes andarieti cotton v Bts. Useable and vegetcottons ": "Affect"bollworm                    
4ml/liter",0.niliprole rahloranth cspray witraps and eromone t phe. Useice and maizf ror pest oer": "Majtem_bor     "s             ter",
  li5g/d 0.amipriwith acet spray aps and trstickyUse yellow es. iseasmit viral dranses": "Tflitewhi      "          ter",
    l 2-3ml/liem oiliter or ne3ml/cloprid 0.with imidaol ntrConting. ing and stuing yellowests caus pSuckingids": "   "aph               ": {
  nfoed_iail "det                 ],
         
     ."ncestaresient oups to prevcal grtate chemiicacy. Ror better eff) fo(5-7 PMing AM) or evenning (6-8 ly mory ear Appler timing. propwithticides ve pesse selectil:** Ucal Contro **Chemi      "⚗️              sts.",
cking pesuroducts for  pem-basedrol and neillar contrpfor cate) (Bts nsi thuringiee Bacillus Usc wasps.arasitid pgs, aninbugs, lacewike ladyrs lpredatoal ge naturl:** EncouraContro*Biological   "🌿 *             t.",
     mpactal id environmenance ane resiststicides peeduced. This rrol if need contmicalally chein fs), andnemiel e(natura control icalen biologieties), thstant varn, resiatiocrop rotactices ( pruralrt with cult(IPM):** StaManagement rated Pest  "🐛 **Integ               [
     onses":      "resp
                   ],"
       resistancees", "nemiatural e, "nontrol"ogical c   "biol        
         "IPM",, cide""pesti, "control""scale", ealybug", ssid", "m, "ja"thrips"                  
  mite", er", "ar", "bor"caterpillitefly",  "wh"aphid",insect", "pest", "                    ": [
keywords "             ": {
  agementest_man         "p
      },           }
          
    es" leavots one sp, whitternodesrt inaves, shomall leency": "Scidefi    "zinc_               
 ls",line soi in alkacommonis), rosloterveinal chen veins (in with greeavesellow lcy": "Yon_deficien       "ir         ent",
    velopmor root deing, poweryed flo, delaveseddish lea"Purple/rency": us_deficiosphor "ph                 y",
  alitr fruit qu stems, pooes, weakedg on leaf rchingwn sco "Broeficiency":otassium_d "p         
          ereals",g in ced tillerinwth, reductunted gro, seaveslder l ostarts fromng wi "Yelloficiency":n_denitroge "                   ": {
_infoiledta  "de          ],
               "
     naturally.ity bilt availaentrid nuealth anrove soil hcompost imprmia and veompost tely. Cctare annual/he-15 tonnes at 10(FYM)e urfarmyard manns:** Use  Solutioic"🌱 **Organ               
     ",tare.0-15 kg/hecrax at 1tare and bokg/hect 25 % Zn) alfate (21c su zinn. Applyoroc and bient in zin are deficlsn soit Indiacrucial. Mosars is y 2-3 yeesting everoil t sRegularagement:** Nutrient Man     "🔬 **             re.",
  /hectakg 40-60 60) at0-0- potash (uriate ofse maf edges), un leiency (browicum deftassi For po kg/hectare. 50-100(46-0-0) aturea Apply ncy. ien deficnitrogeate cally indic typi leavesinglow* Yelsis:*Health AnalyCrop **       "🌿             ses": [
  "respon                ],
       "
        lybdenumn", "mo", "boro"coppernganese", ", "man", "zincnt", "iroutrie "micron           , 
        s""necrosif drop", "lea growth", stuntedg", "inlows", "yelrosi  "chlo              
    , phorus"", "phossiumas"pot", ogentr"ni", eficiencyient d"nutr", ealth "crop h                    [
words":  "key           th": {
   p_heal"cro        
    n {     retur   "
re""gricultuan ase for Indinowledge basive khenmprecod Buil"    ""  t:
   -> Dicf)selbase(dge_nsive_knowleld_comprehe def _bui          
 = {}
 profile  self.user_     y = []
 or_histsationconver       self.e_base()
 dgowle_knrehensiveld_compself._bui= ase _bgef.knowled  self):
      nit__(sel __ief   d
 ""
    "ependencieshout API dwitbot ional chatfoundated ""Advanc
    "hatbot:oundationalCedFancclass Adv""


."sue persistsf the isrt ippoact suion or contstqueing your  try rephrasease

Plticesacral pragricultumon bout comon atirmas
- Infoendationrming recommneral fa
- Geasee bedg my knowle based on advicricultural
- Basic ag**lp with:ill he st**What I canr}

roer** {Error:y}

**er* {user_question:*r QuYou 
**
       . iceI servg to my Aectinnnficulties col difing technicaeriencbut I'm expgize, lo"""I apourn f        ret"""
PI fails when Aesponseack rfallb""Provide        " -> str:
 r: str), errostry: er_querself, usck_response(ba _get_fallef   d    
 ery
rn user_qu      retu
  r_query}" {useon:\nQuestiontext}\nlysis_ct: {anan f"Contexetur           r_context:
 islys  if ana""
      h context" message witPrepare user """tr:
       ) -> sone N str =ontext:analysis_c str, ser_query:(self, uessageuser_mef _prepare_
    d
    y, str(e))_querserresponse(ulback_falf._get_turn sel   re
          e:Exception as  except  
                content
 0].message.ces[nse.choirn respo        retu      
    "
      t.n a momenagain i try  question orhrasing yourry rep tPleaseresponse.  an empty ived but I recee,iz"I apologurn      ret     t:
      ge.conten.messa[0]onse.choicesespf not r i  
         s emptyse iresponf k i     # Chec  
                     )
  0
      00_tokens=1   max           False,
    stream=     
         re,f.temperatuature=selmper te            
   elf.model,model=s             ,
   essagess=mssageme                ate(
crens.ioletompt.cchae = client.   respons
         Get response   #           
      ]
               }
  sis_context)alyer_query, anssage(usmerepare_user__pnt": self.te, "conuser"": "   {"role             mpt},
stem_pro syntent":stem", "coole": "sy"r      {      [
     ges =    messa
        re messages    # Prepa         
          ent)
 t=http_cliiencltp_ey, ht=self.api_kGroq(api_key = ent        cliroq
     import Ggroq  from         nt
  ieq clroalize G     # Initi   
                ut=30.0)
lse, timeoenv=Fat(trust_ httpx.Clientp_client =          htclient
  HTTP    # Create            try:
"
      ling""handced error  enhanwithroq API onse from G""Get resp      "
  tr:= None) -> st: str sis_contex: str, analy_promptystemy: str, s_querserf, uselponse( get_res 
    deflse
        Faurn         retas e:
   Exception ept exc        e.content)
ssagoices[0].mense.ch bool(respourn   ret     
                
    )
        =10x_tokens      ma         alse,
 eam=F       str     
    ure=0.1,    temperat       
     ,self.model   model=            "}],
 "Hello"content": "user", "role": {ges=[sa      mes         
 ons.create(.completi.chatient = cl    response
        uerymple test q Si    #            
t)
        ienp_clnt=httiecley, http_api_ky=self.(api_kelient = Groq  c
          mport Groqoq i  from gr
          .0)eout=10v=False, timst_ent(trux.Clienient = httphttp_cl            :
       try
 ing"""is workction connet if API  """Tes      bool:
 > lf) -onnection(sest_api_cef te   
    d0.7
     e = f.temperatur
        seltant"3.1-8b-ins= "llama-model   self.     y
  api_kef.api_key =sel    str):
    i_key: (self, apnit__
    def __i   
 ng"""li sty andndlingerror haetter  bt withtboed chaasGroq API-bced """Enhan:
    oqChatbots EnhancedGrtime

clast uple
importional, TOpist,  Lrt Dict,g impo typinme
frommport datetitime im date re
fro
importandom
import r
import jsonmport httpx