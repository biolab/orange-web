/**
 * jclass v1.1.9
 * https://github.com/riga/jclass
 *
 * Marcel Rieger, 2015
 * MIT licensed, http://www.opensource.org/licenses/mit-license
 */

(function(factory) {

  /**
   * Make jclass available in any context.
   */

  if (window) {
    // Browser
    window.JClass = factory();

  } else if (typeof(console) == "object" && console.error instanceof Function) {
    // error case
    console.error("cannot determine environment");
  }

})(function() {

  /**
   * Helper functions.
   */

  /**
   * Checks whether a passed object is a function.
   *
   * @param obj - The object to check.
   * @returns {boolean}
   */
  var isFn = function(obj) {
    return obj instanceof Function;
  };

  /**
   * Extends a target object by one or more source objects with shallow key comparisons. Note that
   * the extension is done in-place.
   *
   * @param {object} target - The target object to extend.
   * @param {...object} source - Source objects.
   * @returns {object} The extended object.
   */
  var extend = function(target) {
    var sources = Array.prototype.slice.call(arguments, 1);

    // loop through all sources
    for (var i in sources) {
      var source = sources[i];

      // object check
      if (typeof(source) != "object") {
        continue;
      }

      // loop through all source attributes
      for (var key in source) {
        target[key] = source[key];
      }
    }

    return target;
  };


  /**
   * Default options.
   */

  var defaultOptions = {
    // internal object for indicating that class objects don't have a class object themselves,
    // may not be used by users
    _isClassObject: false
  };


  /**
   * Flags.
   */

  // flag to distinguish between prototype and class instantiation 
  var initializing = false;


  /**
   * Base class definition.
   */

  // empty BaseClass implementation
  var BaseClass = function(){};

  // add the _subClasses entry
  BaseClass._subClasses = [];

  // empty init method
  BaseClass.prototype.init = function(){};


  /**
   * Extend mechanism. Returns a derived class.
   *
   * @param {object} instanceMembers - Members that will be owned by instances.
   * @param {object} classMembers - Members that will be owned by the class itself.
   * @returns {JClass}
   */
  BaseClass._extend = function(instanceMembers, classMembers, options) {

    // default arguments
    if (instanceMembers === undefined) {
      instanceMembers = {};
    }
    if (classMembers === undefined) {
      classMembers = {};
    }
    if (options === undefined) {
      options = {};
    }

    // mixin default options
    options = extend({}, defaultOptions, options);


    // sub class dummy constructor
    var JClass = function() {
      // nothing happens here when we are initializing
      if (initializing) {
        return;
      }

      // store a reference to the class itself
      this._class = JClass;

      // all construction is actually done in the init method
      if (this.init instanceof Function) {
        this.init.apply(this, arguments);
      }
    };


    // alias for readability
    var SuperClass = this;

    // create an instance of the super class via new
    // the flag sandwich prevents a call to the init method
    initializing = true;
    var prototype = new SuperClass();
    initializing = false;

    // get the prototype of the super class
    var superPrototype = SuperClass.prototype;

    // the instance of the super class is our new prototype
    JClass.prototype = prototype;

    // enforce the constructor to be what we expect
    // calls to the constructor will invoke the init method (see above)
    JClass.prototype.constructor = JClass;

    // store a reference to the super class
    JClass._superClass = SuperClass;

    // store references to all extending classes
    JClass._subClasses = [];
    SuperClass._subClasses.push(JClass);

    // make this class extendable as well
    JClass._extend = SuperClass._extend;


    // _extends returns true if the class itself extended "target"
    // in any hierarchy, e.g. every class extends "JClass" itself
    JClass._extends = function(target) {
      // this function operates recursive, so stop when the super class is our BaseClass
      if (this._superClass == BaseClass) {
        return false;
      }

      // success case
      if (target == this._superClass || target == BaseClass) {
        return true;
      }

      // continue with the next super class
      return this._superClass._extends(target);
    };


    // propagate instance members directly to the created protoype,
    // the member is either a normal member or a descriptor
    for (var key in instanceMembers) {
      var property = Object.getOwnPropertyDescriptor(instanceMembers, key);
      var member   = property.value;

      // descriptor flag set?
      if (member !== null && typeof(member) == "object" && member.descriptor) {
        Object.defineProperty(prototype, key, member);

      // getter/setter syntax
      } else if (!("value" in property) && ("set" in property || "get" in property)) {
        Object.defineProperty(prototype, key, property);

      // normal member, simple assignment
      } else {
        prototype[key] = member;

        // if both member and the super member are distinct functions
        // add the super member to the member as "_super"
        var superMember = superPrototype[key];
        if (isFn(member) && isFn(superMember) && member !== superMember) {
          member._super = superMember;
        }
      }
    }


    // propagate class members to the _members object
    if (!options._isClassObject) {
      // try to find the super class of the _members object 
      var ClassMembersSuperClass = SuperClass._members === undefined ?
        BaseClass : SuperClass._members._class;

      // create the actual class of the _members instance
      // with an updated version of our options
      var opts = extend({}, options, { _isClassObject: true });
      var ClassMembersClass = ClassMembersSuperClass._extend(classMembers, {}, opts);

      // store the actual JClass in ClassMembersClass
      ClassMembersClass._instanceClass = JClass;

      // create the _members instance
      JClass._members = new ClassMembersClass();
    }


    // return the new class
    return JClass;
  };


  /**
   * Converts arbitrary protoype-style classes to our JClass definition.
   *
   * @param {function} cls - The class to convert.
   * @returns {JClass}
   */
  BaseClass._convert = function(cls, options) {
    // the properties consist of the class' prototype
    var instanceMembers = cls.prototype;

    // add the constructor function
    instanceMembers.init = function() {
      // simply create an instance of our target class
      var origin = this._origin = BaseClass._construct(cls, arguments);

      // add properties for each own property in _origin
      Object.keys(origin).forEach(function(key) {
        if (!origin.hasOwnProperty(key)) {
          return;
        }

        Object.defineProperty(this, key, {
          get: function() {
            return origin[key];
          }
        });
      }, this);
    };

    // finally, create and return our new class
    return BaseClass._extend(instanceMembers, {}, options);
  };


  /**
   * Returns an instance of a class with a list of arguments. This provides an apply-like
   * constructor usage. Note that this approach does not work with native constructors (e.g. String
   * or Boolean).
   *
   * @param {Class|JClass} cls - The class to instantiate. This may be a JClass or a prototype-based
   *   class.
   * @param {array} [args=[]] - Arguments to pass to the constructor.
   * @returns {instance}
   */
  BaseClass._construct = function(cls, args) {
    // empty default args
    if (args === undefined) {
      args = [];
    }

    // create a class wrapper that calls cls like a function
    var Class = function() {
      return cls.apply(this, args);
    };

    // copy the prototype
    Class.prototype = cls.prototype;

    // return a new instance
    return new Class();
  };


  /**
   * Returns a property descriptor of the super class.
   *
   * @param {JClass|instance} cls - A JClass or an instance of a JClass to retrieve the property
   *   descriptor from.
   * @param {string} prop - The name of the property descriptor to get.
   * @returns {object}
   */
  BaseClass._superDescriptor = function(cls, prop) {
    // if cls is an instance, use its class
    if ("_class" in cls && cls instanceof cls._class) {
      cls = cls._class;
    }

    // a JClass?
    if ("_extends" in cls && cls._extends instanceof Function && cls._extends(this)) {
      return Object.getOwnPropertyDescriptor(cls._superClass.prototype, prop);
    } else {
      return undefined;
    }
  };


  /**
   * Return the BaseClass.
   */

  return BaseClass;
});


/** HashArray
 *
 * Josh Jung,
 * MIT licensed, http://www.opensource.org/licenses/mit-license
 *
 */

/*===========================================================================*\
 * HashArray
\*===========================================================================*/
var HashArray = window.JClass._extend({
  //-----------------------------------
  // Constructor
  //-----------------------------------
  init: function(keyFields, callback, options) {
    keyFields = keyFields instanceof Array ? keyFields : [keyFields];

    this._map = {};
    this._list = [];
    this.callback = callback;

    this.keyFields = keyFields;

    this.isHashArray = true;
    
    this.options = options || {
      ignoreDuplicates: false
    };

    if (callback) {
      callback('construct');
    }
  },
  //-----------------------------------
  // add()
  //-----------------------------------
  addOne: function (obj) {
    var needsDupCheck = false;
    for (var key in this.keyFields) {
      key = this.keyFields[key];
      var inst = this.objectAt(obj, key);
      if (inst) {
        if (this._map[inst]) {
          if (this.options.ignoreDuplicates)
            return;
          if (this._map[inst].indexOf(obj) != -1) {
            // Cannot add the same item twice
            needsDupCheck = true;
            continue;
          }
          this._map[inst].push(obj);
        }
        else this._map[inst] = [obj];
      }
    }

    if (!needsDupCheck || this._list.indexOf(obj) == -1)
      this._list.push(obj);
  },
  add: function() {
    for (var i = 0; i < arguments.length; i++) {
      this.addOne(arguments[i]);
    }

    if (this.callback) {
      this.callback('add', Array.prototype.slice.call(arguments, 0));
    }
    
    return this;
  },
  addAll: function (arr) {
    if (arr.length < 100)
      this.add.apply(this, arr);
    else {
      for (var i = 0; i < arr.length; i++)
        this.add(arr[i]);
    }
    
    return this;
  },
  addMap: function(key, obj) {
    this._map[key] = obj;
    if (this.callback) {
      this.callback('addMap', {
        key: key,
        obj: obj
      });
    }
    
    return this;
  },
  //-----------------------------------
  // Retrieval
  //-----------------------------------
  get: function(key) {
    return (!(this._map[key] instanceof Array) || this._map[key].length != 1) ? this._map[key] : this._map[key][0];
  },
  getAll: function(keys) {
    keys = keys instanceof Array ? keys : [keys];

    if (keys[0] == '*')
      return this.all;

    var res = new HashArray(this.keyFields);
    for (var key in keys)
      res.add.apply(res, this.getAsArray(keys[key]));

    return res.all;
  },
  getAsArray: function(key) {
    return this._map[key] || [];
  },
  getUniqueRandomIntegers: function (count, min, max) {
    var res = [], map = {};

    count = Math.min(Math.max(max - min, 1), count);
    
    while (res.length < count)
    {
      var r = Math.floor(min + (Math.random() * (max + 1)));
      if (map[r]) continue;
      map[r] = true;
      res.push(r);
    }

    return res;
  },
  //-----------------------------------
  // Peeking
  //-----------------------------------
  has: function(key) {
    return this._map.hasOwnProperty(key);
  },
  //-----------------------------------
  // Utility
  //-----------------------------------
  objectAt: function(obj, path) {
    if (typeof path === 'string') {
      return obj[path];
    }

    var dup = path.concat();
    // else assume array.
    while (dup.length && obj) {
      obj = obj[dup.shift()];
    }

    return obj;
  },
  //-----------------------------------
  // Iteration
  //-----------------------------------
  forEach: function(keys, callback) {
    keys = keys instanceof Array ? keys : [keys];

    var objs = this.getAll(keys);

    objs.forEach(callback);
    
    return this;
  },
  forEachDeep: function(keys, key, callback) {
    keys = keys instanceof Array ? keys : [keys];

    var self = this,
      objs = this.getAll(keys);

    objs.forEach(function (item) {
      callback(self.objectAt(item, key), item);
    });
    
    return this;
  },
  //-----------------------------------
  // Filtering
  //-----------------------------------
  filter: function (keys, callbackOrKey) {
    var self = this;
    
    var callback = (typeof(callbackOrKey) == 'function') ? callbackOrKey : defaultCallback;

    var ha = new HashArray(this.keyFields);
    ha.addAll(this.getAll(keys).filter(callback));
    return ha;
    
    function defaultCallback(item) {
      var val = self.objectAt(item, callbackOrKey);
      return val !== undefined && val !== false;
    }
  }
});

//-----------------------------------
// Operators
//-----------------------------------
Object.defineProperty(HashArray.prototype, 'all', {
  get: function () {
    return this._list;
  }
});

Object.defineProperty(HashArray.prototype, 'map', {
  get: function () {
    return this._map;
  }
});


/** TrieSearch
 *
 * Josh Jung,
 * MIT licensed, http://www.opensource.org/licenses/mit-license
 *
 */

var MAX_CACHE_SIZE = 64;

var TrieSearch = function (keyFields, options) {
  this.options = options || {};

  // Default ignoreCase to true
  this.options.ignoreCase = (this.options.ignoreCase === undefined) ? true : this.options.ignoreCase;
  this.options.maxCacheSize = this.options.maxCacheSize || MAX_CACHE_SIZE;
  this.options.cache = this.options.hasOwnProperty('cache') ? this.options.cache : true;
  this.options.splitOnRegEx = this.options.hasOwnProperty('splitOnRegEx') ? this.options.splitOnRegEx : /\s/g;

  this.keyFields = keyFields ? (keyFields instanceof Array ? keyFields : [keyFields]) : [];
  this.root = {};
  this.size = 0;
  this.getCache = new HashArray('key');
};

TrieSearch.prototype = {
  add: function (obj) {
    if (this.options.cache)
      this.clearCache();
    
    for (var k in this.keyFields)
    {
      var key = this.keyFields[k],
        val = obj[key];
        
      if (!val) continue;
      
      val = val.toString();

      // add without splitting first
      if (this.options.ignoreCase) {
        this.map(val.toLowerCase(), obj);
      }
      else {
        this.map(val, obj);
      }

      // possible regex split
      if (this.options.splitOnRegEx !== undefined)
      {
        phrases = val.split(this.options.splitOnRegEx);

        var i;
        if (this.options.ignoreCase) {
          for (i = 0, l = phrases.length; i < l; i++)
            this.map(phrases[i].toLowerCase(), obj)
        }
        else {
          for (i = 0, l = phrases.length; i < l; i++)
            this.map(phrases[i], obj)
        }
      }
      else this.map(val, obj);
    }
  },
  reset: function () {
    this.root = {};
    this.size = 0;
  },
  clearCache: function () {
    this.getCache = new HashArray('key');
  },
  cleanCache: function () {
    while (this.getCache.all.length > this.options.maxCacheSize)
      this.getCache.remove(this.getCache.all[0]);
  },
  addFromObject: function (obj, valueField) {
    if (this.options.cache)
      this.clearCache();

    valueField = valueField || 'value';

    if (this.keyFields.indexOf('_key_') == -1)
      this.keyFields.push('_key_');

    for (var key in obj)
    {
      var o = {_key_: key};
      o[valueField] = obj[key];
      this.add(o);
    }
  },
  map: function (key, value) {
    if (this.options.cache)
      this.clearCache();

    var keyArr = this.keyToArr(key),
      self = this;

    insert(keyArr, value, this.root);

    function insert(keyArr, value, node) {
      if (keyArr.length == 0)
      {
        node['value'] = node['value'] || [];
        node['value'].push(value);
        return; 
      }

      var k = keyArr.shift();

      if (!node[k])
        self.size++;

      node[k] = node[k] || {};

      insert(keyArr, value, node[k])
    }
  },
  keyToArr: function (key) {
    var keyArr;
      
    if (this.options.min && this.options.min > 1)
    {
      if (key.length < this.options.min)
        return [];

      keyArr = [key.substr(0, this.options.min)];
      keyArr = keyArr.concat(key.substr(this.options.min).split(''));
    }
    else keyArr = key.split('');

    return keyArr;
  },
  findNode: function (key) {
    if (this.options.min > 0 && key.length < this.options.min)
      return [];

    return f(this.keyToArr(key), this.root);

    function f(keyArr, node) {
      if (!node) return undefined;
      if (keyArr.length == 0) return node;

      var k = keyArr.shift();
      return f(keyArr, node[k]);
    }
  },
  _get: function (phrase) {
    phrase = this.options.ignoreCase ? phrase.toLowerCase() : phrase;
    
    var c;
    if (this.options.cache && (c = this.getCache.get(phrase)))
      return c.value;

    var ret = undefined,
      haKeyFields = this.options.indexField ? [this.options.indexField] : this.keyFields;
      words = this.options.splitOnRegEx ? phrase.split(this.options.splitOnRegEx) : [phrase];

    for (var w = 0, l = words.length; w < l; w++)
    {
      if (this.options.min && words[w].length < this.options.min)
        continue;

      var temp = new HashArray(haKeyFields);

      if (node = this.findNode(words[w]))
        aggregate(node, temp);

      ret = ret ? ret.intersection(temp) : temp;
    }
    
    var v = ret ? ret.all : [];

    if (this.options.cache)
    {
      this.getCache.add({key: phrase, value: v});
      this.cleanCache();
    }

    return v;
    
    function aggregate(node, ha) {
      if (node.value && node.value.length)
        ha.addAll(node.value);

      for (var k in node)
        if (k != 'value')
          aggregate(node[k], ha);
    }
  },
  get: function (phrases) {
    var self = this,
      haKeyFields = this.options.indexField ? [this.options.indexField] : this.keyFields,
      ret = undefined;

    phrases = (phrases instanceof Array) ? phrases : [phrases];

    for (var i = 0, l = phrases.length; i < l; i++)
    {
      var temp = this._get(phrases[i]);
      ret = ret ? ret.addAll(temp) : new HashArray(haKeyFields).addAll(temp);
    }
    
    return ret.all;
  }
};

window.TrieSearch = TrieSearch;
