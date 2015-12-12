# simpl
simpl is a "Security IMplied Password Locker"

As stated, simpl is a password locker. The idea behind it is a small, lightweight, but secure, password locker.

simpl has not been audited; therefore, you are admonished to use at your own risk. It has been developed with the best cryptographic libraries available for Python and any security issues brought to my attention will be taken care of ASAP.

In regards to not being audited, I welcome anyone to audit it, if they wish. Until a proper audit has been performed, it is in your best interest to not rely on the security of this software and treat it as potentially insecure. 

I have developed simpl to learn more about cryptography and its practical applications.

If you want to contribute, please keep in mind that your additions must stay within the realm of "Simple and Lightweight".

# Security Limitations
If you read the [Cryptography Library's](https://cryptography.io/en/latest/) documentaion, you will see the following warning:

> Memory wiping is used to protect secret data or key material from attackers with access to uninitialized memory. This can be either because the attacker has some kind of local user access or because of how other software uses uninitialized memory.

> Python exposes no API for us to implement this reliably and as such almost all software in Python is potentially vulnerable to this attack. The CERT secure coding guidelines assesses this issue as “Severity: medium, Likelihood: unlikely, Remediation Cost: expensive to repair” and we do not consider this a high risk for most users.

I have included the above warning to showcase Python's shortcomings when it comes to cryptographic applications. Again, as stated above, use at your own risk.
