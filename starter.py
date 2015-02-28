# coding: utf-8

import io
import string
from FE_Dict import FE_Dict
import nltk
from nltk.tag.stanford import POSTagger
from ngram_downloader import get_bigram_probabilities
import time

# I have already added environment variables as

# CLASSPATH = D:/stanford-postagger/stanford-postagger.jar
# STANFORD_MODELS =  D:/stanford-postagger/models/

all_bigram_probabilities = {
    (u'aboard', u'the'): 2.2757267288397998e-06,
    (u'aboard', u'them'): 1.2457356479700366e-08,
    (u'along', u'the'): 7.138120781746693e-05,
    (u'along', u'them'): 1.3757288286342373e-07,
    (u'call', u'chiefly'): 2.448088051720809e-10,
    (u'call', u'mainly'): 4.357645633223939e-10,
    (u'call', u'mostly'): 4.162485911507474e-10,
    (u'call', u'primarily'): 9.888704854965624e-10,
    (u'call', u'principally'): 1.5167837472129797e-10,
    (u'chiefly', u'aboard'): 5.879337988679012e-11,
    (u'chiefly', u'along'): 1.6978557226821067e-08,
    (u'chiefly', u'during'): 1.5849606960216533e-08,
    (u'chiefly', u'in'): 1.288660996578983e-06,
    (u'chiefly', u'inside'): 4.747965492990502e-10,
    (u'chiefly', u'into'): 1.5099132166795926e-08,
    (u'chiefly', u'on'): 5.882770466314469e-07,
    (u'chiefly', u'within'): 1.2857066078453272e-08,
    (u'discover', u'chiefly'): 1.6649943576640958e-10,
    (u'discover', u'primarily'): 0.0,
    (u'discover', u'principally'): 1.222816847779029e-10,
    (u'during', u'the'): 0.00016666997544234619,
    (u'during', u'them'): 3.0596190470078e-08,
    (u'fat', u'meat'): 4.2884840567580795e-08,
    (u'fats', u'themselves'): 6.264749274897952e-10,
    (u'find', u'chiefly'): 1.8206313678881259e-09,
    (u'find', u'mainly'): 3.220810063098156e-09,
    (u'find', u'mostly'): 5.160009974858326e-09,
    (u'find', u'primarily'): 6.852683143154792e-10,
    (u'find', u'principally'): 8.665888284742351e-10,
    (u'fleshy', u'meat'): 8.715291266447878e-10,
    (u'get', u'chiefly'): 4.992528751524006e-10,
    (u'get', u'it', u'chiefly'): 0.0,
    (u'get', u'it', u'mainly'): 1.3350648017662614e-10,
    (u'get', u'it', u'mostly'): 4.2127569488403793e-10,
    (u'get', u'mainly'): 1.0572991371304852e-09,
    (u'get', u'mostly'): 4.8571440203204475e-09,
    (u'get', u'primarily'): 3.86606482938312e-10,
    (u'get', u'principally'): 5.879337988679012e-11,
    (u'greases', u'himself'): 7.83093659362244e-11,
    (u'herself', u'call'): 2.187721892532579e-09,
    (u'herself', u'discover'): 3.9648717642393194e-10,
    (u'herself', u'find'): 2.0068922634841613e-09,
    (u'herself', u'get'): 3.57613885171304e-08,
    (u'herself', u'hit'): 1.2144087124799086e-09,
    (u'herself', u'work'): 1.2825919770698135e-09,
    (u'himself', u'call'): 5.72176950264236e-09,
    (u'himself', u'come', u'up', u'with'): 5.241765910213303e-10,
    (u'himself', u'discover'): 2.0849562076818984e-09,
    (u'himself', u'find'): 7.311922178843133e-09,
    (u'himself', u'get'): 4.453943169835384e-08,
    (u'himself', u'get', u'it'): 3.1833991692709063e-10,
    (u'himself', u'hit'): 6.069834856958778e-09,
    (u'himself', u'locate'): 2.939668994339506e-11,
    (u'himself', u'work'): 4.7533967872936955e-09,
    (u'hit', u'chiefly'): 5.879337988679012e-11,
    (u'hit', u'mainly'): 5.825026017092227e-10,
    (u'hit', u'mostly'): 1.395238369283902e-09,
    (u'hit', u'primarily'): 1.2722204192905373e-10,
    (u'hit', u'principally'): 2.4456337996414668e-11,
    (u'in', u'the'): 0.003831017413176596,
    (u'in', u'them'): 1.7105862298194552e-05,
    (u'inside', u'the'): 2.1938265490462072e-05,
    (u'inside', u'them'): 3.930768173177057e-07,
    (u'into', u'the'): 0.00041121564572677016,
    (u'into', u'them'): 2.6820545144801144e-06,
    (u'locate', u'chiefly'): 7.83093659362244e-11,
    (u'locate', u'mainly'): 1.420430977699949e-10,
    (u'locate', u'mostly'): 5.879337988679012e-11,
    (u'locate', u'primarily'): 4.750419502208558e-10,
    (u'mainly', u'aboard'): 8.324971788320479e-11,
    (u'mainly', u'along'): 4.492229344066345e-08,
    (u'mainly', u'during'): 7.987290828737059e-08,
    (u'mainly', u'in'): 2.9586896062028245e-06,
    (u'mainly', u'inside'): 5.54167600697042e-09,
    (u'mainly', u'into'): 3.871293330348635e-08,
    (u'mainly', u'on'): 1.988295480259694e-06,
    (u'mainly', u'within'): 6.419007902991325e-08,
    (u'mostly', u'aboard'): 8.665888284742351e-10,
    (u'mostly', u'along'): 3.6312007622996134e-08,
    (u'mostly', u'during'): 5.799501678893648e-08,
    (u'mostly', u'in'): 2.2897801272847573e-06,
    (u'mostly', u'inside'): 7.10019154581687e-09,
    (u'mostly', u'into'): 2.1535289107532662e-08,
    (u'mostly', u'on'): 9.187786815800791e-07,
    (u'mostly', u'within'): 6.13084658596108e-08,
    (u'on', u'the'): 0.0015217759646475315,
    (u'on', u'them'): 1.579110403326922e-05,
    (u'predominately', u'along'): 4.162485911507474e-10,
    (u'predominately', u'during'): 5.385302759286503e-10,
    (u'predominately', u'in'): 3.044300900256758e-08,
    (u'predominately', u'into'): 2.49749144975997e-10,
    (u'predominately', u'on'): 1.0354602508755306e-08,
    (u'predominately', u'within'): 1.0429689611957116e-09,
    (u'primarily', u'aboard'): 1.9095577202810077e-10,
    (u'primarily', u'along'): 2.979652613532835e-08,
    (u'primarily', u'during'): 5.789323331839569e-08,
    (u'primarily', u'in'): 2.635499981806788e-06,
    (u'primarily', u'inside'): 3.5204535953070604e-09,
    (u'primarily', u'into'): 2.8142149055554455e-08,
    (u'primarily', u'on'): 2.772052539512515e-06,
    (u'primarily', u'within'): 1.0297165076167403e-07,
    (u'principally', u'along'): 8.233591142214891e-09,
    (u'principally', u'during'): 1.1595708393485893e-08,
    (u'principally', u'in'): 6.007872741520259e-07,
    (u'principally', u'inside'): 3.132374637448976e-10,
    (u'principally', u'into'): 6.768942517609844e-09,
    (u'principally', u'on'): 3.3676131749871274e-07,
    (u'principally', u'within'): 1.1488983542307096e-08,
    (u'saturated', u'fats'): 2.2713421543585355e-07,
    (u'that', u'saturated'): 3.213617283392978e-08,
    (u'the', u'fat'): 3.173529080413573e-06,
    (u'the', u'fattish'): 5.580462481002968e-10,
    (u'the', u'fleshy'): 2.517636872312323e-07,
    (u'them', u'fat'): 1.847211184013986e-08,
    (u'them', u'fleshy'): 2.546895021271478e-10,
    (u'themselves', u'call'): 1.8196401718739708e-08,
    (u'themselves', u'come', u'up', u'with'): 1.0216818779884562e-09,
    (u'themselves', u'discover'): 3.0832166819649842e-09,
    (u'themselves', u'find'): 1.8983453919929616e-08,
    (u'themselves', u'get'): 2.711796120991039e-08,
    (u'themselves', u'get', u'it'): 5.651602970335734e-11,
    (u'themselves', u'hit'): 1.3655962471936789e-09,
    (u'themselves', u'locate'): 1.958961291792516e-10,
    (u'themselves', u'work'): 1.3756978223256056e-08,
    (u'these', u'saturated'): 2.4283266508717816e-09,
    (u'this', u'saturated'): 6.055013823669242e-09,
    (u'within', u'the'): 0.0001320709998253733,
    (u'within', u'them'): 1.915805796670611e-06,
    (u'work', u'chiefly'): 1.284865813744318e-08,
    (u'work', u'mainly'): 5.3978256531195257e-08,
    (u'work', u'mostly'): 3.5146756616200037e-08,
    (u'work', u'predominately'): 6.072043562399543e-10,
    (u'work', u'primarily'): 8.077705615505693e-08,
    (u'work', u'principally'): 6.261036133992093e-09,
    (u'a', u'banning'): 6.883552172709528e-09,
    (u'a', u'forbidding'): 1.0210739986860062e-07,
    (u'a', u'lid'): 4.5696427264374506e-07,
    (u'a', u'prohibition'): 5.436962169369508e-07,
    (u'a', u'suppression'): 1.205979209828456e-07,
    (u'incur', u'a'): 2.402644412313748e-07,
    (u'incur', u'an'): 5.535523683874999e-08,
    (u'incur', u'one'): 2.961916489852001e-09,
    (u'outlawry', u'at'): 8.371921211836053e-10,
    (u'outlawry', u'by'): 1.6296756166767068e-09,
    (u'outlawry', u'in'): 6.504617511282618e-09,
    (u'outlawry', u'to'): 2.3201297549846345e-09,
    (u'outlawry', u'upon'): 9.883796420195878e-10,
    (u'outlawry', u'with'): 3.9648717642393194e-10,
    (u'suppression', u'at'): 1.6552149872950395e-08,
    (u'suppression', u'by'): 1.1545297340376237e-07,
    (u'suppression', u'in'): 1.578706232407967e-07,
    (u'suppression', u'to'): 2.822764066934269e-08,
    (u'suppression', u'upon'): 8.567080933552518e-10,
    (u'suppression', u'with'): 2.892426209655241e-08,
    (u'they', u'incur'): 7.922203693055963e-08,
    (u'those', u'incur'): 1.7613471445243611e-10,
    (u'against', u'him'): 1.1201846064068377e-05,
    (u'against', u'it'): 6.993919896558509e-06,
    (u'against', u'the'): 0.00012227011393406428,
    (u'anti', u'it'): 2.1047175113864114e-10,
    (u'anti', u'the'): 5.615536036174262e-09,
    (u'football', u'must'): 2.0123234745206275e-09,
    (u'him', u'football'): 4.945579501480779e-10,
    (u'it', u'football'): 2.7516902090241047e-09,
    (u'must', u'battle'): 2.7203450159163367e-08,
    (u'must', u'combat'): 2.0201085249027528e-08,
    (u'must', u'cope'): 8.796000727784303e-08,
    (u'must', u'fight'): 5.048168674193221e-07,
    (u'must', u'strive'): 3.0372031289971346e-07,
    (u'must', u'struggle'): 1.5092119554083183e-07,
    (u'must', u'war'): 4.366299322100531e-09,
    (u'must', u'wrestle'): 3.200649700829672e-08,
    (u'the', u'football'): 1.3341557973944873e-06,
    (u'the', u'racism'): 2.870684596700812e-07,
    (u'versus', u'him'): 8.959854802537137e-10,
    (u'versus', u'it'): 2.1397909555354033e-09,
    (u'versus', u'the'): 2.237987700937083e-06,
    (u'at', u'employees'): 1.1303950220309389e-08,
    (u'boost', u'him'): 7.57747442570178e-09,
    (u'boost', u'it'): 2.1014525231066727e-08,
    (u'boost', u'the'): 6.190233534653089e-07,
    (u'by', u'employees'): 5.787983923255524e-07,
    (u'expand', u'him'): 9.053753302623591e-10,
    (u'expand', u'it'): 1.8179969174525468e-07,
    (u'expand', u'the'): 3.0359035463334294e-06,
    (u'extend', u'him'): 1.1846684522254236e-08,
    (u'extend', u'it'): 3.6856887675185135e-07,
    (u'extend', u'the'): 4.78543370263651e-06,
    (u'firm', u'enhance'): 1.958961291792516e-10,
    (u'firm', u'increase'): 4.1424791374922165e-09,
    (u'firm', u'raise'): 1.140548822053944e-09,
    (u'firm', u'rise'): 7.638230881124031e-10,
    (u'grow', u'him'): 2.4085651251226636e-09,
    (u'grow', u'it'): 1.3863653691714717e-07,
    (u'it', u'business'): 2.0608434070368276e-08,
    (u'it', u'company'): 2.6909515504769388e-08,
    (u'it', u'enterprise'): 3.8191154405620154e-10,
    (u'it', u'firm'): 5.4705383334408e-08,
    (u'it', u'undertaking'): 3.8191154405620154e-10,
    (u'of', u'a'): 0.0010604157578200102,
    (u'of', u'an'): 0.00020530694746412337,
    (u'of', u'one'): 7.505855319323018e-05,
    (u'off', u'employees'): 4.8410615960392533e-08,
    (u'out', u'of', u'employees'): 4.701490308178791e-09,
    (u'pay', u'at'): 3.6058999342003517e-07,
    (u'pay', u'by'): 2.1511750958325138e-07,
    (u'pay', u'from'): 1.8732550444156004e-07,
    (u'pay', u'of'): 7.682841669520712e-07,
    (u'pay', u'off'): 2.032532165685552e-06,
    (u'pay', u'out', u'of'): 7.929865475375664e-08,
    (u'pay', u'than'): 8.864435585564934e-08,
    (u'pay', u'to'): 2.2980764242674923e-06,
    (u'pay', u'with'): 2.6402499031519255e-07,
    (u'screw', u'at'): 3.706454165808282e-08,
    (u'screw', u'by'): 1.3112492425193523e-08,
    (u'screw', u'from'): 1.7612426184143715e-08,
    (u'screw', u'off'): 6.833903443137501e-09,
    (u'screw', u'out', u'of'): 6.4468890226265785e-09,
    (u'screw', u'than'): 2.432285262088385e-09,
    (u'screw', u'with'): 7.445336436262551e-08,
    (u'than', u'employees'): 6.337236868603213e-08,
    (u'the', u'attempt'): 5.672923862221069e-06,
    (u'the', u'business'): 3.137721250823233e-05,
    (u'the', u'company'): 5.305028935254086e-05,
    (u'the', u'enterprise'): 4.337893187766895e-06,
    (u'the', u'firm'): 1.6853002307470888e-05,
    (u'the', u'salary'): 1.0908360081884894e-06,
    (u'the', u'undertaking'): 1.1650913904759364e-06,
    (u'the', u'venture'): 1.2304935239626502e-06,
    (u'to', u'a'): 0.0004525906406342983,
    (u'to', u'an'): 8.739766053622589e-05,
    (u'undertaking', u'grow'): 4.8912675992829335e-11,
    (u'wage', u'at'): 4.9088276554698496e-08,
    (u'wage', u'off'): 6.70692668069961e-10,
    (u'wage', u'out', u'of'): 1.1660803433954925e-09,
    (u'with', u'employees'): 4.801055837333479e-07,
    (u'at', u'her'): 5.006340506952256e-05,
    (u'at', u'it'): 1.629040161787998e-05,
    (u'at', u'there'): 5.4704122121052023e-08,
    (u'by', u'a'): 0.00024367946025449783,
    (u'by', u'her'): 2.299518382642418e-05,
    (u'by', u'it'): 1.002220096779638e-05,
    (u'by', u'there'): 1.7898715753972283e-07,
    (u'close', u'at'): 1.7557847513671732e-06,
    (u'close', u'by'): 3.2541914833927876e-06,
    (u'close', u'from'): 4.285989341212826e-08,
    (u'close', u'of'): 6.9631103087886e-06,
    (u'close', u'off'): 1.956388757662353e-07,
    (u'close', u'out', u'of'): 6.4171639113652645e-09,
    (u'close', u'than'): 2.992651193522988e-08,
    (u'close', u'to'): 4.493400592764374e-05,
    (u'close', u'with'): 7.444820369073568e-07,
    (u'earth', u'by'): 4.887470055336962e-07,
    (u'earth', u'from'): 5.411173589209284e-07,
    (u'earth', u'of'): 5.373539551101203e-07,
    (u'earth', u'to'): 2.108218779994786e-06,
    (u'earth', u'with'): 1.0950710986890044e-06,
    (u'he', u'joined'): 2.1110816987857106e-06,
    (u'her', u'biologic'): 4.014275301056358e-10,
    (u'her', u'biological'): 1.4450267826759955e-07,
    (u'him', u'joined'): 6.0740390495084284e-09,
    (u'himself', u'joined'): 2.6975458311540024e-08,
    (u'his', u'biologic'): 1.3169289547754204e-09,
    (u'his', u'biological'): 1.6791913992619811e-07,
    (u'it', u'joined'): 1.7560668652549793e-07,
    (u'its', u'biologic'): 8.608321833136756e-09,
    (u'its', u'biological'): 1.6610096054137102e-07,
    (u'joined', u'a'): 1.0291892067471053e-06,
    (u'joined', u'her'): 8.099874548861408e-07,
    (u'joined', u'it'): 1.8946480651038655e-07,
    (u'joined', u'the'): 1.1317524695186876e-05,
    (u'joined', u'there'): 3.2402002858589185e-08,
    (u'meet', u'her'): 2.582745310064638e-06,
    (u'near', u'from'): 1.1621146267515314e-08,
    (u'near', u'of'): 5.990764684327132e-08,
    (u'near', u'to'): 5.397223503678106e-06,
    (u'off', u'a'): 8.757851446716813e-06,
    (u'off', u'it'): 8.232034645061503e-07,
    (u'off', u'the'): 6.249763464438729e-05,
    (u'off', u'there'): 2.518721871069829e-07,
    (u'out', u'of', u'a'): 1.3042392311035655e-05,
    (u'out', u'of', u'her'): 8.537228495697491e-06,
    (u'out', u'of', u'it'): 7.759016853015055e-06,
    (u'out', u'of', u'the'): 0.0001111834280891344,
    (u'out', u'of', u'there'): 1.361989120596263e-06,
    (u'people', u'at'): 4.716794592241058e-06,
    (u'people', u'by'): 1.9000734141627618e-06,
    (u'people', u'from'): 8.192223958758404e-06,
    (u'people', u'off'): 3.507329893182032e-07,
    (u'people', u'out', u'of'): 7.388759399873379e-07,
    (u'people', u'than'): 1.1198694664926734e-06,
    (u'people', u'with'): 1.4036991615284933e-05,
    (u'than', u'a'): 7.142700633266941e-05,
    (u'than', u'the'): 0.0001428159375791438,
    (u'than', u'there'): 1.4777808701182948e-06,
    (u'that', u'he'): 0.0003198664780938998,
    (u'that', u'him'): 7.523670220166423e-08,
    (u'that', u'himself'): 1.283208810320957e-07,
    (u'that', u'it'): 0.0002484044889570214,
    (u'the', u'city'): 8.021900430321693e-05,
    (u'the', u'place'): 4.737427116197068e-05,
    (u'the', u'town'): 3.5900011425837874e-05,
    (u'trace', u'her'): 8.559354469639402e-08,
    (u'trace', u'his'): 1.5864329583337167e-07,
    (u'trace', u'its'): 2.3130164095164218e-07,
    (u'where', u'him'): 4.087398863816816e-09,
    (u'where', u'himself'): 5.3097249930189605e-09,
    (u'where', u'it'): 2.971816957142437e-05,
    (u'wherein', u'he'): 6.777806902391603e-07,
    (u'wherein', u'himself'): 6.753876069520715e-10,
    (u'wherein', u'it'): 2.9631944897801077e-07,
    (u'whither', u'he'): 5.586534683743594e-07,
    (u'with', u'a'): 0.0005581100995186716,
    (u'with', u'her'): 8.710779729881324e-05,
    (u'with', u'it'): 4.176695802016184e-05,
    (u'with', u'the'): 0.0009926558705046773,
    (u'with', u'there'): 1.440041046407714e-07,
    (u'a', u'block'): 3.489392952360504e-06,
    (u'a', u'installment'): 1.3216239214131065e-10,
    (u'a', u'piece'): 2.036529349425109e-05,
    (u'a', u'round'): 3.882121177412046e-06,
    (u'a', u'slab'): 4.487274054554291e-07,
    (u'a', u'slat'): 1.7578580369104202e-08,
    (u'a', u'slice'): 1.3002887158108933e-06,
    (u'a', u'sliver'): 2.700961942991853e-07,
    (u'a', u'steak'): 2.7669597102431e-07,
    (u'a', u'tranche'): 2.5112050217046544e-08,
    (u'a', u'wafer'): 1.2982836494757066e-07,
    (u'accomodate', u'by'): 7.336901225452053e-11,
    (u'at', u'her'): 5.006340506952256e-05,
    (u'at', u'herself'): 7.232855239180935e-07,
    (u'at', u'it'): 1.629040161787998e-05,
    (u'at', u'she'): 3.011059668267535e-08,
    (u'at', u'that'): 4.2111865695915185e-05,
    (u'at', u'this'): 5.7461562391836196e-05,
    (u'by', u'it'): 1.002220096779638e-05,
    (u'by', u'she'): 1.2179825148450618e-07,
    (u'by', u'that'): 1.4121014828560874e-05,
    (u'by', u'this'): 2.97252136078896e-05,
    (u'contain', u'at'): 2.8499219695277134e-07,
    (u'contain', u'by'): 1.024097429080939e-08,
    (u'contain', u'upon'): 1.1010260481114642e-09,
    (u'contain', u'with'): 5.972254912833819e-09,
    (u'her', u'bachelor'): 7.039007954290355e-08,
    (u'her', u'lone'): 1.8902690079869444e-08,
    (u'her', u'unaccompanied'): 1.013326866861064e-09,
    (u'her', u'very'): 2.5329065920232097e-06,
    (u'herself', u'alone'): 2.2081777473204056e-07,
    (u'herself', u'lonely'): 2.824077527385782e-09,
    (u'herself', u'mere'): 5.382848611290569e-10,
    (u'herself', u'only'): 8.097280357333148e-08,
    (u'herself', u'only', u'one'): 1.0069103884013941e-09,
    (u'herself', u'single'): 2.016772970847569e-09,
    (u'herself', u'sole'): 1.1501841423733339e-09,
    (u'hold', u'at'): 2.898208606438857e-07,
    (u'hold', u'by'): 1.9178015975285234e-07,
    (u'hold', u'in'): 2.1805475398650742e-06,
    (u'hold', u'in', u'in'): 3.085254621226774e-11,
    (u'hold', u'in', u'to'): 1.386955411630808e-10,
    (u'hold', u'to'): 1.2186749813736242e-06,
    (u'hold', u'upon'): 8.076972051185294e-07,
    (u'hold', u'with'): 3.926911773532993e-07,
    (u'in', u'her'): 0.00012181573401903734,
    (u'in', u'herself'): 5.922184698192723e-07,
    (u'off', u'that'): 1.5467081198039523e-06,
    (u'off', u'this'): 1.3119950494910881e-06,
    (u'out', u'of', u'that'): 2.634192355799314e-06,
    (u'out', u'of', u'this'): 5.5180130402732175e-06,
    (u'piece', u'at'): 2.297755088420672e-07,
    (u'piece', u'off'): 5.43597398205975e-08,
    (u'piece', u'out', u'of'): 7.437696680767658e-08,
    (u'piece', u'than'): 2.750137628737548e-08,
    (u'round', u'at'): 7.630773666278401e-07,
    (u'round', u'by'): 5.237218232423402e-07,
    (u'round', u'from'): 2.9659110367674657e-07,
    (u'round', u'off'): 1.8364085008215625e-07,
    (u'round', u'out', u'of'): 1.0745887291108147e-08,
    (u'round', u'than'): 3.049741703620157e-08,
    (u'round', u'to'): 3.5131221238771104e-06,
    (u'round', u'with'): 1.3127204852025898e-06,
    (u'slab', u'by'): 1.2786887548799086e-08,
    (u'slab', u'from'): 2.1377688952384233e-08,
    (u'slab', u'of'): 6.627038544593233e-07,
    (u'slab', u'to'): 5.096847210950273e-08,
    (u'subdue', u'at'): 2.4268539955407675e-09,
    (u'subdue', u'by'): 8.055493161407412e-09,
    (u'subdue', u'in'): 6.425817433708403e-09,
    (u'subdue', u'to'): 8.002130957862619e-09,
    (u'subdue', u'with'): 4.370994233227066e-09,
    (u'tame', u'at'): 6.141731123676664e-09,
    (u'tame', u'in'): 3.9232992854465465e-08,
    (u'tame', u'to'): 3.4317301000896805e-08,
    (u'tame', u'with'): 7.977183580365477e-09,
    (u'than', u'that'): 3.437538362049963e-05,
    (u'than', u'this'): 7.827733952581184e-06,
    (u'tranche', u'at'): 2.39374420285543e-09,
    (u'tranche', u'by'): 1.4345157284267884e-09,
    (u'tranche', u'from'): 2.3013499439450413e-09,
    (u'tranche', u'of'): 5.40096465329043e-08,
    (u'tranche', u'than'): 4.747965492990502e-10,
    (u'tranche', u'to'): 5.947798475958166e-09,
    (u'tranche', u'with'): 8.289162023444874e-09,
    (u'with', u'her'): 8.710779729881324e-05,
    (u'with', u'herself'): 1.098699158319505e-06,
    (u'with', u'it'): 4.176695802016184e-05,
    (u'with', u'she'): 3.9664765694169546e-08,
    (u'with', u'that'): 3.251677208027104e-05,
    (u'with', u'this'): 4.3344109144527465e-05,
    (u'although', u'at'): 7.529493473157345e-07,
    (u'although', u'by'): 3.512262054528037e-07,
    (u'although', u'in'): 2.8289354077060125e-06,
    (u'although', u'to'): 3.075247292372296e-07,
    (u'although', u'upon'): 1.6580106620978086e-08,
    (u'although', u'with'): 5.067564359251264e-07,
    (u'but', u'at'): 1.5178165540419286e-05,
    (u'but', u'by'): 1.4873898635414662e-05,
    (u'but', u'in'): 4.871895544056315e-05,
    (u'but', u'to'): 3.4967457395396195e-05,
    (u'but', u'upon'): 1.3036752193329448e-06,
    (u'but', u'with'): 1.979433454835089e-05,
    (u'by', u'a'): 0.00024367946025449783,
    (u'by', u'her'): 2.299518382642418e-05,
    (u'by', u'it'): 1.002220096779638e-05,
    (u'by', u'the'): 0.0009408732294104993,
    (u'by', u'there'): 1.7898715753972283e-07,
    (u'the', u'astonishment'): 4.963497701737651e-07,
    (u'the', u'surprise'): 1.6174172401406395e-06,
    (u'upon', u'a'): 2.377171676926082e-05,
    (u'upon', u'her'): 1.2526888440334005e-05,
    (u'upon', u'it'): 1.3216984825703548e-05,
    (u'upon', u'the'): 0.00013608365043182857,
    (u'upon', u'there'): 2.8263727358535107e-08,
    (u'a', u'contamination'): 4.785904827997456e-08,
    (u'a', u'dirtiness'): 1.4439056617021606e-09,
    (u'a', u'pollution'): 9.603207118402679e-08,
    (u'at', u'good'): 1.531544882027447e-07,
    (u'at', u'right'): 2.7314698627378675e-06,
    (u'at', u'well'): 1.2524468928631904e-07,
    (u'drive', u'at'): 2.2144553213365725e-07,
    (u'drive', u'by'): 3.095449869761069e-07,
    (u'drive', u'in'): 9.5267685651379e-07,
    (u'drive', u'to'): 3.616869548750401e-06,
    (u'drive', u'upon'): 8.996432487862194e-09,
    (u'drive', u'with'): 4.0737988626915467e-07,
    (u'in', u'their'): 0.0001792054099496454,
    (u'it', u'contamination'): 4.945579501480779e-10,
    (u'it', u'pollution'): 1.581253794569193e-09,
    (u'off', u'good'): 2.1283576678854388e-08,
    (u'off', u'well'): 1.5253513652169204e-07,
    (u'offensive', u'at'): 5.0918300686930706e-08,
    (u'offensive', u'by'): 8.183761224245245e-08,
    (u'offensive', u'upon'): 1.3260733899844723e-09,
    (u'offensive', u'with'): 4.0031087777947505e-08,
    (u'out', u'of', u'good'): 6.55693188633677e-08,
    (u'out', u'of', u'right'): 7.817431812995324e-09,
    (u'out', u'of', u'well'): 8.213889568509103e-09,
    (u'than', u'good'): 1.0262850764775067e-06,
    (u'than', u'right'): 1.5174758516423026e-07,
    (u'than', u'well'): 1.274294660902342e-07,
    (u'the', u'contamination'): 4.2741577033211797e-07,
    (u'the', u'dirtiness'): 1.604252553022434e-08,
    (u'the', u'pollution'): 6.512859442864283e-07,
    (u'there', u'contamination'): 2.448088051720809e-10,
    (u'there', u'pollution'): 2.49749144975997e-10,
    (u'to', u'their'): 0.00011468989032437094,
    (u'with', u'right'): 7.098437038166594e-07,
    (u'I', u'have'): 0.0002874531128327362,
    (u'a', u'band'): 3.7641860899384483e-06,
    (u'a', u'batch'): 8.149596908424428e-07,
    (u'a', u'cluster'): 2.3944119220686844e-06,
    (u'a', u'group'): 3.275183826190187e-05,
    (u'a', u'party'): 1.370806603517849e-05,
    (u'a', u'unit'): 4.134254368182155e-06,
    (u'an', u'band'): 5.778076767049001e-10,
    (u'an', u'group'): 5.434951821925438e-09,
    (u'and', u'repel'): 1.3141369947788917e-07,
    (u'desired', u'enter'): 0.0,
    (u'have', u'desired'): 3.98797311618182e-07,
    (u'have', u'intended'): 3.962644683497274e-07,
    (u'have', u'required'): 1.0177461717830738e-06,
    (u'in', u'him'): 1.4023917174199596e-05,
    (u'inside', u'it'): 1.062884450675483e-06,
    (u'inside', u'the'): 2.1938265490462072e-05,
    (u'into', u'him'): 1.8275197817274602e-06,
    (u'into', u'it'): 1.1104472378065111e-05,
    (u'into', u'the'): 0.00041121564572677016,
    (u'me', u'and'): 3.098638080700766e-05,
    (u'myself', u'and'): 4.088321475137491e-06,
    (u'on', u'him'): 1.7652800124778878e-05,
    (u'on', u'it'): 2.7863966352015268e-05,
    (u'on', u'the'): 0.0015217759646475315,
    (u'party', u'by'): 3.632058849234454e-07,
    (u'party', u'from'): 6.287667986271117e-07,
    (u'party', u'of'): 6.017073019393138e-06,
    (u'party', u'to'): 6.274684665186214e-06,
    (u'party', u'with'): 1.0715814369177679e-06,
    (u'peg', u'me'): 2.3845997398908025e-09,
    (u'peg', u'myself'): 4.8912675992829335e-11,
    (u'probably', u'a'): 3.4054156685670023e-06,
    (u'probably', u'an'): 5.975623480480863e-07,
    (u'probably', u'one'): 6.920507189533964e-07,
    (u'shut', u'out', u'me'): 8.217951319444694e-11,
    (u'unit', u'at'): 3.3086330120113416e-07,
    (u'unit', u'by'): 1.529297364299964e-07,
    (u'unit', u'from'): 1.9152232511032707e-07,
    (u'unit', u'off'): 9.448000160006131e-09,
    (u'unit', u'out', u'of'): 1.4127316649847899e-08,
    (u'unit', u'than'): 4.6977884693433225e-08,
    (u'unit', u'with'): 4.4283603983785724e-07,
    (u'within', u'him'): 2.416316021935927e-06,
    (u'within', u'it'): 3.797290787588281e-06,
    (u'within', u'the'): 0.0001320709998253733,
    (u'at', u'right'): 2.7314698627378675e-06,
    (u'at', u'that'): 4.2111865695915185e-05,
    (u'at', u'this'): 5.7461562391836196e-05,
    (u'be', u'yet'): 3.409951858657223e-07,
    (u'by', u'right'): 1.2490207836890477e-06,
    (u'by', u'that'): 1.4121014828560874e-05,
    (u'by', u'this'): 2.97252136078896e-05,
    (u'elected', u'at'): 2.0252775101425868e-07,
    (u'elected', u'by'): 1.9771314896388503e-06,
    (u'elected', u'from'): 2.526928994939226e-07,
    (u'elected', u'of'): 1.128593885013629e-08,
    (u'elected', u'off'): 2.8384077033205557e-10,
    (u'elected', u'out', u'of'): 1.4906472056708253e-08,
    (u'elected', u'than'): 7.283752712083924e-09,
    (u'elected', u'to'): 3.7481059962374275e-06,
    (u'elected', u'with'): 8.209327972963365e-08,
    (u'from', u'right'): 9.811683980842645e-07,
    (u'in', u'that'): 9.495186895946972e-05,
    (u'in', u'this'): 0.00029637443367391825,
    (u'of', u'left'): 1.19105214935189e-06,
    (u'of', u'right'): 4.8760844038042706e-06,
    (u'off', u'right'): 1.901156139183513e-07,
    (u'out', u'of', u'right'): 7.817431812995324e-09,
    (u'right', u'be'): 6.6639522344758e-08,
    (u'right', u'exist'): 3.0150333341083524e-09,
    (u'than', u'right'): 1.5174758516423026e-07,
    (u'the', u'elected'): 7.472598326785374e-07,
    (u'them', u'elected'): 1.4045514529215097e-08,
    (u'this', u'competition'): 2.524025433103816e-07,
    (u'to', u'right'): 4.501389639699482e-06,
    (u'to', u'that'): 6.706151543767191e-05,
    (u'upon', u'that'): 3.5327370824234094e-06,
    (u'upon', u'this'): 7.461376753781224e-06,
    (u'with', u'right'): 7.098437038166594e-07,
    (u'with', u'that'): 3.251677208027104e-05,
    (u'with', u'this'): 4.3344109144527465e-05,
    (u'a', u'along', u'with'): 1.392144455270028e-09,
    (u'a', u'to'): 8.450070367871376e-07,
    (u'a', u'together', u'with'): 2.029669821101976e-09,
    (u'a', u'with'): 2.3670416737786582e-07,
    (u'an', u'along', u'with'): 1.9521157607060857e-10,
    (u'an', u'to'): 8.73786447641578e-08,
    (u'an', u'together', u'with'): 1.9521157607060857e-10,
    (u'an', u'with'): 2.5334152553568856e-08,
    (u'at', u'her'): 5.006340506952256e-05,
    (u'at', u'him'): 3.5099834349239245e-05,
    (u'at', u'it'): 1.629040161787998e-05,
    (u'at', u'sound'): 5.03252444161717e-08,
    (u'at', u'the'): 0.0009149648249149323,
    (u'get', u'to', u'at'): 4.13604839266668e-09,
    (u'get', u'to', u'by'): 1.2451348396780304e-08,
    (u'get', u'to', u'with'): 3.996788899840453e-09,
    (u'he', u'herself'): 9.688636837257292e-10,
    (u'he', u'himself'): 7.537701094406657e-06,
    (u'he', u'themselves'): 6.069589275625731e-10,
    (u'him', u'herself'): 1.1527899346219783e-07,
    (u'him', u'himself'): 6.187375589661315e-08,
    (u'him', u'themselves'): 2.3881379540569014e-08,
    (u'himself', u'herself'): 1.5708822576065984e-09,
    (u'himself', u'himself'): 3.94461963093562e-09,
    (u'himself', u'themselves'): 3.6215012932938606e-10,
    (u'in', u'him'): 1.4023917174199596e-05,
    (u'in', u'it'): 4.4820011680712923e-05,
    (u'in', u'the'): 0.003831017413176596,
    (u'it', u'herself'): 5.647513887652167e-07,
    (u'it', u'himself'): 1.4475734815277974e-06,
    (u'it', u'themselves'): 5.970032646018808e-07,
    (u'its', u'body'): 1.201122415750433e-06,
    (u'its', u'corpse'): 1.3480809357702128e-08,
    (u'off', u'her'): 5.8374648688186426e-06,
    (u'off', u'his'): 1.1280649232503492e-05,
    (u'off', u'its'): 1.3216957199801982e-06,
    (u'off', u'sound'): 2.1462443378084117e-08,
    (u'out', u'of', u'her'): 8.537228495697491e-06,
    (u'out', u'of', u'his'): 1.584078609084827e-05,
    (u'out', u'of', u'its'): 2.44998454945744e-06,
    (u'out', u'of', u'sound'): 1.478306188573697e-08,
    (u'pardon', u'by'): 3.741187093453391e-08,
    (u'pardon', u'upon'): 6.75734379562698e-09,
    (u'pardon', u'with'): 2.3936737036933664e-08,
    (u'than', u'a'): 7.142700633266941e-05,
    (u'than', u'an'): 1.1020528745575575e-05,
    (u'than', u'one'): 2.8116931389376987e-05,
    (u'that', u'one'): 3.942366674891673e-05,
    (u'to', u'him'): 0.00012794327267329209,
    (u'to', u'it'): 5.91052867093822e-05,
    (u'to', u'the'): 0.0025328685296699405,
    (u'by', u'a'): 0.00024367946025449783,
    (u'by', u'her'): 2.299518382642418e-05,
    (u'by', u'it'): 1.002220096779638e-05,
    (u'by', u'the'): 0.0009408732294104993,
    (u'by', u'there'): 1.7898715753972283e-07,
    (u'cluster', u'east'): 2.2035246544094278e-10,
    (u'cluster', u'is'): 3.943856086152664e-07,
    (u'commune', u'is'): 2.1731921151513234e-08,
    (u'east', u'remained'): 3.44214423630973e-09,
    (u'eastern', u'remained'): 5.385302793980973e-11,
    (u'for', u'a', u'long', u'time', u'a'): 5.138500647206001e-08,
    (u'for', u'a', u'long', u'time', u'her'): 4.7602018993231354e-09,
    (u'for', u'a', u'long', u'time', u'it'): 6.247935147030148e-08,
    (u'for', u'a', u'long', u'time', u'the'): 1.7055211287697603e-07,
    (u'for', u'a', u'long', u'time', u'there'): 2.4985346236405803e-08,
    (u'from', u'her'): 4.3513313357834704e-05,
    (u'game', u'at'): 6.319183114555926e-07,
    (u'game', u'by'): 3.2664095783729863e-07,
    (u'game', u'from'): 2.121372943975075e-07,
    (u'game', u'of'): 5.690355919796275e-06,
    (u'game', u'than'): 1.4964830086228176e-07,
    (u'game', u'to'): 1.1759724429794005e-06,
    (u'game', u'with'): 1.2413570971148147e-06,
    (u'is', u'remained'): 3.3687751477273764e-09,
    (u'judge', u'few'): 2.939668994339506e-11,
    (u'judge', u'no'): 2.313980473900301e-08,
    (u'judge', u'not', u'very'): 1.695480908447955e-10,
    (u'long', u'-', u'standing', u'a'): 2.4875264348356296e-10,
    (u'long', u'-', u'standing', u'the'): 6.646206363036811e-10,
    (u'longtime', u'a'): 4.794914743033729e-10,
    (u'longtime', u'it'): 1.958961291792516e-10,
    (u'longtime', u'the'): 4.305787948410966e-10,
    (u'parcel', u'from'): 5.925125279304666e-08,
    (u'parcel', u'of'): 2.2452579742093803e-06,
    (u'parcel', u'to'): 8.087297942438454e-08,
    (u'reckon', u'little'): 6.264749274897952e-10,
    (u'remained', u'wanting'): 5.333444935695653e-10,
    (u'remained', u'without'): 1.4953452875943185e-07,
    (u'section', u'at'): 6.496044022696879e-07,
    (u'section', u'off'): 1.5438021083724607e-08,
    (u'section', u'out', u'of'): 1.2278136729548805e-08,
    (u'section', u'than'): 3.3111973607447e-08,
    (u'section', u'with'): 6.24409437932627e-07,
    (u'she', u'assess'): 1.1360993812381537e-09,
    (u'she', u'decide'): 2.5951482740538268e-08,
    (u'she', u'decree'): 1.6155907861525876e-10,
    (u'she', u'judge'): 5.722014861930802e-09,
    (u'she', u'reckon'): 1.41920383778249e-09,
    (u'she', u'rule'): 3.112367807922567e-09,
    (u'she', u'try'): 8.450730604181445e-08,
    (u'slice', u'at'): 2.7315084416557056e-08,
    (u'slice', u'by'): 1.563787588310106e-08,
    (u'slice', u'from'): 6.53247695936443e-08,
    (u'slice', u'of'): 2.192286956415046e-06,
    (u'slice', u'off'): 6.883012204639272e-08,
    (u'slice', u'out', u'of'): 2.1471863398403457e-08,
    (u'slice', u'than'): 2.78084144600399e-09,
    (u'slice', u'to'): 4.963101218891097e-08,
    (u'slice', u'with'): 4.76446171404632e-08,
    (u'than', u'the'): 0.0001428159375791438,
    (u'try', u'bit'): 1.6649943576640958e-10,
    (u'try', u'few'): 1.860154183463969e-10,
    (u'try', u'little'): 1.4342703691383463e-09,
    (u'try', u'no'): 1.9772746995272428e-08,
    (u'with', u'a'): 0.0005581100995186716,
    (u'with', u'her'): 8.710779729881324e-05,
    (u'with', u'it'): 4.176695802016184e-05,
    (u'with', u'the'): 0.0009926558705046773,
    (u'with', u'there'): 1.440041046407714e-07,
    (u'without', u'reaction'): 1.7384156336675005e-08
}


def preprocess_words(sentence):
    # Convert apostrophes to 'e ', such that
    # L'enterprise  => Le enterprise
    # D'un          => De un
    sentence = sentence.replace(u'’', 'e ')
    sentence = sentence.replace('\'', 'e ')

    # Break words separated by a dash into two separate words
    sentence = sentence.replace('-', ' ')

    # Removing newlines/whitespace
    sentence = sentence.strip()

    # Remove all punctuation inside the sentence. We need to loop through the
    # characters of the string because this is a unicode string and we cannot
    # use the .translate() method on a unicode string.
    sentence = "".join([ch for ch in sentence if ch not in string.punctuation])
    return sentence.lower().split(' ')

def baseline_translate(sentence, fe_dict):
    words = preprocess_words(sentence)
    translation = []

    for word in words:
        t = fe_dict.translate(word)
        translation.append(t[0])

    return " ".join(translation)

def pos_order_strategy(sentence, fe_dict):
    words = preprocess_words(sentence)
    st = POSTagger(r'stanford-postagger/models/french.tagger', r'stanford-postagger/stanford-postagger.jar', encoding="utf-8"    )
    # print "round"
    # print words
    tokens = st.tag(words)
    # print tokens
    last_word_type = ""
    last_word = ""
    post_order = tokens

    # Invert tokens if they show up in (NOUN, ADJ) order to be (ADJ, NOUN)
    adjs = ['ADJ']
    nouns = ['NC','N']
    for i in range(1, len(post_order)):
        prev_word, prev_word_type = post_order[i-1]
        curr_word, curr_word_type = post_order[i]

        if (prev_word_type in nouns) and (curr_word_type in adjs):
            post_order[i] = (prev_word, prev_word_type)
            post_order[i-1] = (curr_word, curr_word_type)

    # Invert tokens if they show up as (REFLEXIVE PRONOUN, VERB) to be
    # (VERB, REFLEXIVE PRONOUN)
    verbs = ["V", "VIMP", "VINF", "VPP", "VPR", "VS"]
    reflexive_pronouns = ['CLO']
    for i in range(1, len(post_order)):
        prev_word, prev_word_type = post_order[i-1]
        curr_word, curr_word_type = post_order[i]

        if (prev_word_type in reflexive_pronouns) and (curr_word_type in verbs):
            post_order[i] = (prev_word, prev_word_type)
            post_order[i-1] = (curr_word, curr_word_type)


    # print " ".join(post_order)
    words = [word for word, word_type in post_order]
    translation = translate_by_picking_best_bigrams(words, fe_dict)
    return " ".join(translation)
    # print "end"
    # tokens = nltk.word_tokenize(processed_sentence)
    # print tokens

def get_cross_product_bigrams(first_list, second_list):
    result = []
    for first_list_word in first_list:
        for second_list_word in second_list:
            result.append((first_list_word, second_list_word))
    return result

# Gets all possible bigrams for the sentence based on all pairs of
# all possible translations for each word pair
def get_all_bigrams_in_sentence(words, fe_dict):
    all_bigrams = []
    for i in range(1, len(words)):
        prev_word_translations = fe_dict.translate(words[i-1])
        curr_word_translations = fe_dict.translate(words[i])
        bigrams = get_cross_product_bigrams(prev_word_translations, curr_word_translations)
        all_bigrams.extend(bigrams)
    return all_bigrams

def find_best_bigram(bigrams, bigram_probabilities):
    most_probable_bigram = ("", "")
    highest_probability = -1.0

    for bigram in bigrams:
        if bigram in bigram_probabilities:
            probability = bigram_probabilities[bigram]
            if probability > highest_probability:
                most_probable_bigram = bigram
                highest_probability = probability

    if highest_probability == -1.0:
        return bigrams[0]

    return most_probable_bigram


def translate_by_picking_best_bigrams(words, fe_dict):
    translation = words

    if len(words) == 0:
        return translation
    elif len(words) == 1:
        # Translate the only word and pick the best unigram.
        only_word = words[0]
        t = fe_dict.translate(only_word)
        translation.append(t[0])
        return translation
    # Otherwise, we have at least two words, and can use the regular procedure.
    else:
        # all_bigrams_in_sentence = get_all_bigrams_in_sentence(words, fe_dict)
        # print all_bigrams_in_sentence
        # all_bigram_probabilities = get_bigram_probabilities(all_bigrams_in_sentence)

        for i in range(1, len(words)):
            # If we are looking at the first two words, go ahead and just find
            # out which translated bigram pair out of the possible translation
            # bigram pairs ranks the highest on Google's NGrams
            if (i == 1):
                # Create the list of bigrams as a list of tuples [(String, String)]
                first_word_translations = fe_dict.translate(words[i-1])
                second_word_translations = fe_dict.translate(words[i])
                bigrams = get_cross_product_bigrams(first_word_translations, second_word_translations)

                # Get the best bigram and use that
                best_first_word, best_second_word = find_best_bigram(bigrams, all_bigram_probabilities)
                translation[i-1] = best_first_word
                translation[i] = best_second_word
            else:
                prev_word = translation[i-1]
                current_word_translations = fe_dict.translate(words[i])
                bigrams = get_cross_product_bigrams([prev_word], current_word_translations)

                # 'prev_word' cannot possibly have changed from earlier since we passed
                # in a list of size one to the first argument for get_cross_product_bigrams
                prev_word, best_curr_word = find_best_bigram(bigrams, all_bigram_probabilities)
                translation[i] = best_curr_word

        return translation

def main():
    fe_dict = FE_Dict()

    with io.open("data/dev_set.txt", 'r', encoding="utf-8") as f:
        for line in f:
            baseline = baseline_translate(line, fe_dict)
            print baseline
            pos_translation = pos_order_strategy(line, fe_dict)
            print pos_translation

if __name__ == '__main__':
	main()