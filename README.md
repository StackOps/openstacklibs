# openstacklibs
## What is openstacklibs

OpenStacklibs is a set of python libraries used to develop backoffice components needed when building an OpenStack service with Business Support Services. This libraries can be bundled in 3 different groups:

### OpenStack management
Sometimes the OpenStack python libraries add a complexity to the final component that does not justify its use. That's why we have developed several helper libraries that can manage some specific parts of Openstack. Warning: we only implement a small subset of the capabilities, and these capabilities only used for us.

### StackOps management
StackOps Portal and Chargeback have a rich REST API. We have develop some libraries that wraps this API followinf the same approach of OpenStack management components. Again, there is no full coverage of capabilities.

### Third party tools
We also have integrated our solutions with third party tools like Mailing systems, WHMCS or Zendesk.

## This is a work in progress
Please use it as a reference of how to integrate Openstack with third party components, not as a full & complete guide of Openstack integration.
