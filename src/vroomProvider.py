import multiprocessing
import requests

class VroomProvider:
    GET_ITEM_TEMPLATE = "https://my.microsoftpersonalcontent.com:443/personal/{}/_api/v2.0/drives/{}/items/{}?expand=children(filter%3DremoteItem/folder%20ne%20null%20or%20folder%20ne%20null;select%3Daudio,bundle,commentSettings,createdDateTime,createdBy,dataLossPrevention,deleted,eTag,file,fileSystemInfo/lastAccessedDateTime,folder,id,image,lastModifiedDateTime,location,malware,name,package,parentReference,photo,reactions,remoteItem,root,shared,shareditem_internal_xschema_storage_live_com,sharepointIds,size,specialFolder,vault,video,webDavUrl,file/originalMetadata,photoStreamItemSource),tags(select%3DautoTagged,name,localizedName),lenses&select=audio,bundle,commentSettings,createdDateTime,createdBy,dataLossPrevention,deleted,eTag,file,fileSystemInfo/lastAccessedDateTime,folder,id,image,lastModifiedDateTime,location,malware,name,package,parentReference,photo,reactions,remoteItem,root,shared,shareditem_internal_xschema_storage_live_com,sharepointIds,size,specialFolder,vault,video,webDavUrl,file/originalMetadata,photoStreamItemSource"
    # GET_ALL_ITEMS_TEMPLATE = "https://my.microsoftpersonalcontent.com:443/personal/{}/_api/v2.0/drives/view.delta"

    def __init__(self, cid, auth):
        self.session = requests.Session()

        self.setCID(cid)
        self.setAuth(auth)
    
    def setCID(self, cid):
        self.cid = cid
    
    def setAuth(self, auth):
        self.auth = auth
    
    def loadSingleItem(self, item_id):
        url = self.GET_ITEM_TEMPLATE.format(self.cid, self.cid, item_id)
        return self.fetch_url(url)
    
    def loadAllItemsV1(self, itemIds):
        with multiprocessing.Pool(processes=len(itemIds)) as pool:
            responses = pool.map(self.loadSingleItem, itemIds)
            result = {"value":responses}
            return result

    '''
    def loadAllItemsV2(self, filterBy=None):
        url = self.GET_ALL_ITEMS_TEMPLATE.format(self.cid, self.cid)
        try:
            response = self.session.get(url, headers={"authorization": self.auth})
            response.raise_for_status()
            items = response.json()
            if filterBy:
                return self.filterByItemId(items, filterBy)
            else:
                return items
        except requests.exceptions.RequestException as e:
            print(f"Error fetching all items: {e}")
            return None
    '''
    
    def filterByItemId(items, itemIds):
        itemIdsSet = set(itemIds)
        return [i for i in items if i["id"] in itemIdsSet]

    def fetch_url(self, url, item_id=None):
        try:
            response = self.session.get(url, headers={"authorization": self.auth})
            response.raise_for_status()
            item = response.json()
            return item
        except requests.exceptions.RequestException as e:
            if item_id:
                print(f"Error fetching item {item_id}: {e}")
            else:
                print(f"Error fetching all items: {e}")
            return None
