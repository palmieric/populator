# populator
An utility to populate a 3scale instance with synthetic data.<br>
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
    <li>The services are not promoted to staging neither production</li>
    <li>The services are not intended to be consistent or working</li>
    <li>It doesn't work with 3scale amp <= 2.5</li>
</ul>

<b>Install and run</b>
<p>The only requirement is to have python3 installed.</p>
<p>To run <b>populator</b>:
<ul>
    <li>clone the repo:
        <ul>
            <li>git clone https://github.com/palmieric/populator.git</li>
        </ul>
    </li>
    <li>cd into the directory:
        <ul>
            <li>cd populator</li>
        </ul>
    </li>
    <li>install the requirements:
        <ul>
            <li>python3 -m pip install -r requirements.txt</li>
        </ul>
    </li>
    <li>run:
        <ul>
            <li>./populator.py --help</li>
            or
            <li>python3 populator.py --help</li>
        </ul>
    </li>
</ul>



