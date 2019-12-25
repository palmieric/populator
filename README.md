# populator
An utility to populate a 3scale installation with synthetic data.<br>
The tool will create:<br>
<ul>
    <li> N services (default: 1)</li>
    <li> 1 metric per service</li>
    <li> N rules per service (default: 1)</li>
    <li> N application plans per service (default: 1)</li>
    <li> N application per service (default: 1)</li>
</ul>

<b>Populator</b> will create the applications under a (random) already existent account picking one of the application plan created.

<b>Known issues:</b>
<ul>
    <li>The api errors are not handled</li>
    <li>The services are not promoted to staging neither production</li>
    <li>The services are not intended to be consistent or working</li>
</ul>
