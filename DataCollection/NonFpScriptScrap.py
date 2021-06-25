import requests
import pandas as py
# from Effivetech import Wordslist


RawData = py.read_csv(r"prefilteredtop10kjsfiles.csv");
counter = 13932;
Defaulter_Websites = [];
DataExcel = [];
for row in RawData.index:

    CurrentURL = RawData['URL'][row]
    # CurrentURL = 'https://dss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/js/lib/jquery-1-edb203c114.10.2.js'
    if CurrentURL.find('.js') != -1 and CurrentURL.find('http') != -1:   # basic filtering
        # print(CurrentURL);
        try:   # Creating Session and Header
            s = requests.Session()
            s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36';
            response = s.get(CurrentURL,timeout = 6.0);
            print('got response for :' + CurrentURL);
        # Removing record which are not Not available
        except requests.ConnectionError as e:
            continue;
        except requests.Timeout as e:
            continue;
        except requests.TooManyRedirects as e:
            continue;
        except requests.exceptions.RequestException as e:
            continue;
        except Exception:
            continue;
        # print(response.status_code)
        if response.status_code == 200:
            string1 = response.text;
            # if (any(word in string1 for word in Wordslist)):
            #     Defaulter_Websites.append([CurrentURL,'wordpresent']);
            #     print(CurrentURL + ' wordpresent');
            # else:
            FileName = "Data1/NonBrowser_Fingerprint_Script_" + str(counter) + ".js";   # Storing th files with names
            f = open(FileName, "w", encoding="utf-8")
            f.write(response.text + "")
            f.close();
            counter = counter + 1;
            print(counter)

        else:
            Defaulter_Websites.append([CurrentURL,'failedreq']);   # Extracting URL which found to have Not available
            print(CurrentURL + ' failedreq');
        # break;

Defaulter_Websites_Data = py.DataFrame(Defaulter_Websites, columns=['Defaulter_URLs','reason'])
Defaulter_Websites_Data.to_csv('Defaulter_Good_Websites_Data.csv')













































































































































































Wordslist = [
    'onpointerleave',
'StereoPannerNode'	,
'FontFaceSetLoadEvent',
'PresentationConnectionAvailableEvent',
'MediaDeviceInfo',
'msGetRegionContent',
'peerIdentity'	,
'MSManipulationEvent',
'VideoStreamTrack'	,
'mozSetImageElement',
'magnetometer'	,
'requestWakeLock',
'PresentationRequest',
'audioWorklet'	,
'onwebkitanimationiteration'	,
'onpointerenter'	,
'onwebkitanimationstart',
'onlostpointercapture',
'RTCCertificate',
'PresentationConnectionList',
'onMSVideoOptimalLayoutChanged'	,
'PresentationAvailability'	,
'BaseAudioContext'	,
'activeVRDisplays'	,
'BluetoothRemoteGATTCharacteristic',
'VisualViewport',
'PresentationConnection'	,
'onMSVideoFormatChanged'	,
'onMSVideoFrameStepCompleted'	,
'BluetoothDevice',
'onuserproximity',
'ongotpointercapture',
'onpointerout'	,
'accelerometer'	,
'chargingchange'	,
'onafterscriptexecute'	,
'channelCountMode'		,
'getDevices'	,
'maxChannelCount'	,
'baseLatency'	,
'onpointerover'	,
'onbeforescriptexecute'	,
'onicegatheringstatechange'	,
'MediaDevices'	,
'numberOfInputs',
'channelInterpretation',
'speedOfSound'	,
'dopplerFactor'	,
'midi'	,
'ondeviceproximity',
'HTMLMenuItemElement'	,
'updateCommands'	,
'FRAGMENT_SHADER_DERIVATIVE_HINT_OES'	,
'getSupportedProfiles'	,
'initCompositionEvent'	,
'initAnimationEvent'	,
'vrdisplayfocus'	,
'initTransitionEvent'	,
'vrdisplayblur'	,
'exportKey'	,
'onauxclick',
'microphone',
'iceGatheringState',
'ondevicelight'	,
'renderedBuffer',
'WebGLContextEvent',
'ondeviceorientationabsolute',
'startRendering',
'createOscillator',
'knee',
'OfflineAudioContext',
'timeLog',
'getFloatFrequencyData',
'WEBGL_compressed_texture_atc',
'illuminance',
'reduction'	,
'modulusLength',
'WebGL2RenderingContext',
'enumerateDevices'	,
'AmbientLightSensor',
'attack'	,
'AudioWorklet',
'Worklet'	,
'AudioWorkletNode'	,
'lastStyleSheetSet'	,
'DeviceProximityEvent',
'DeviceLightEvent'	,
'enableStyleSheetsForSet'	,
'UserProximityEvent'	,
'vrdisplaydisconnect'	,
'mediaDevices'	,
'vibrate'	,
'vendorSub'	,
'setValueAtTime',
'getChannelData',
'MAX_DRAW_BUFFERS_WEBGL',
'reliable'	,
'WEBGL_draw_buffers',
'EXT_sRGB'	,
'setSinkId'	,
'namedCurve',
'minDecibels'	,
'UNKNOWN_ERR'	,
'WEBGL_debug_shaders',
'productSub'	,
'hardwareConcurrency',
'publicExponent'	,
'requestMIDIAccess'	,
'mozIsLocallyAvailable',
'ondevicemotion',
'maxDecibels'	,
'getLayoutMap'	,
'Animatable'	,
'GeckoActiveXObject',
'XPathResult'	,
'mozBattery'	,
'IndexedDB'	,
'generateKey'	,
'buildID'	,
'getSupportedExtensions',
'MAX_TEXTURE_MAX_ANISOTROPY_EXT',
'oscpu',
'oninvalid'	,
'vpn'	,
'lastEventID',
'mozCaptureStream',
'createDynamicsCompressor',
'privateKey',
'EXT_texture_filter_anisotropic',
'isPointInPath'	,
'getContextAttributes',
'BatteryManager',
'getShaderPrecisionFormat',
'depthFunc'	,
'uniform2f'	,
'rangeMax'	,
'rangeMin'	,
'EXT_disjoint_timer_query',
'scrollByPages'	,
'CanvasCaptureMediaStreamTrack',
'onlanguagechange'	,
'RTCDataChannelEvent'	,
'onMSFullscreenChange'	
'clearColor'	,
'createWriter'	,
'getUniformLocation',
'getAttribLocation'	,
'drawArrays'	,
'useProgram',
'enableVertexAttribArray',
'createShader',
'compileShader',
'shaderSource',
'attachShader',
'bufferData',
'linkProgram',
'vertexAttribPointer',
'bindBuffer',
'createProgram',
'OES_standard_derivatives',
'appCodeName',
'getAttributeNodeNS',
'ARRAY_BUFFER'	,
'suffixes'	,
'TouchEvent',
'MIDIPort'	,
'MAX_COLOR_ATTACHMENTS_WEBGL',
'lowpass'	,
'onaudioprocess',
'showModalDialog',
'globalStorage'	,
'camera',
'onanimationiteration'	,
'webkitNotification'	,
'textBaseline'	,
'MediaStreamTrackEvent',
'deviceproximity',
'taintEnabled'	,
'alphabetic'	,
'userproximity'	,
'globalCompositeOperation'	,
'outputBuffer',
'WebGLUniformLocation',
'WebGLShaderPrecisionFormat',
'OffscreenCanvas',
'MIDIInput'	,
'ServiceWorkerContainer',
'pranswer'	,
'ScriptProcessorNode'	,
'MIDIAccess'	,
'vrdisplayconnect'	,
'customelements'	,
'SVGAnimationElement',
'createScriptProcessor'	,
'createBuffer'	,
'UIEvent'	,
'toSource'	,
'createAnalyser',
'fillRect'	,
'requestAutocomplete'	,
'evenodd'	,
'fillText'	,
'candidate'	,
'WEBGL_debug_renderer_info'	,
'toDataURL'	,
'dischargingTime'	,
'bluetooth'	,
'vrdisplaydeactivate'	,
'MediaKeySession'	,
'vrdisplayactivate'	,
'FLOAT'	,
'battery',
'devicelight',
'onanimationstart',
'getExtension',
'onemptied'	,
'captureStream'	,
'MediaStreamTrack'	,
'WebGLRenderingContext',
'oncomplete',
'onratechange'	,
'fillStyle'	,
'getGamepads',
'BiquadFilterNode',
'SVGZoomEvent'	,
'filterNumber'	,
'NotSupported'	,
'PermissionStatus'	,
'ignoreBOM'	,
'queryInfo'	,
'onspeechend'	,
'maxTouchPoints',
'frequencyBinCount',
'credential'	,
'iceTransportPolicy',
'iceCandidatePoolSize',
'DeviceMotionEvent'	,
'rtcpMuxPolicy'	,
'webgl',
'indexedDB'	,
'rotationAngle',
'setTargetAtTime'	,
'iceServers',
'clipboard'	,
'onconnectionstatechange'	,
'connectionstatechange'	,
'meetOrSlice'	,
'remoteCandidateId'	,
'channelCount'	,
'getParameter'	,
'selectionDirection',
'closePath'	,
'NetworkInformation'	,
'emma'	,
'createOffer'	,
'languages'	,
'setLocalDescription',
'requestFileSystem'	,
'createDataChannel'	,
'onicecandidate'	,
'Float32Array'	,
'requestPointerLock'	,
'ValidityState'	,
'onwebkitresourcetimingbufferfull'	,
'gathering'	,
'MediaQueryList'	,
'tooltipNode'	,
'drawWindow'	,
'Sensor'	,
'TEMPORARY'	,
'SpeechRecognition'	,
'recognition'	,
'beginPath'	,
'smoothingTimeConstant'	,
'systemLanguage'	,
'acceleration'	,
'multiply'	,
#'arc'	,
'fonts'	,
'gbk'	,
'outerText',
'deriveBits',
'doNotTrack',
'publicKey'	,
'storageArea',
'EMS'	,
'xMaxYMin',
'DataError',
'remoteId',
'RTCPeerConnection',
'createMediaStreamSource'	,
'getImageData'	,
'bundlePolicy'	,
'PERSISTENT'	,
'ANGLE_instanced_arrays'	,
'hasPointerCapture'	,
'focusMode'	,
'xMidYMin'
]
